from datetime import date

from django.db.models import F, Sum

from calories.apps.calorie.models import DayMeal, Meal, NutritionalDayGoal, NutritionalGoal
from utils.food import get_food_calories


def get_user_day_meals(user):
    user_meals = Meal.objects.filter(creator=user)
    meals = []

    for meal in user_meals.all():
        meal_query = get_meal_day_goal_query(user, meal).prefetch_related('foods')

        if meal_query.exists():
            today_meal = meal_query.annotate(
                total_calories=Sum(
                    (F('foods__serving_amount') / F('foods__food__number_of_units')) * F('foods__food__calories'))
            ).first()
        else:
            today_meal = DayMeal.objects.create(meal=meal)
        meals.append(today_meal)

    return meals


def get_user_day_nutrients(user, nutrients):
    meals = get_user_day_meals(user)

    result = {}

    for meal in meals:
        for meal_food in meal.foods.all():
            for nutrient in nutrients:
                nutrient_value = get_nutrient_value(meal_food, nutrient)
                result[nutrient] = result.get(nutrient, 0) + nutrient_value

    return result


def get_nutrient_value(meal_food, name):
    food = meal_food.food
    food_nutrient = getattr(food, name)
    food_amount = food.number_of_units
    multiplier = meal_food.serving_amount / food_amount
    return multiplier * food_nutrient


def get_nutritional_day_goal_query(user, goal=None):
    today = date.today()

    if not goal:
        goal = NutritionalGoal.objects.filter(creator=user, active=True).first()

    return NutritionalDayGoal.objects.filter(
        creator=user,
        created__year=today.year,
        created__month=today.month,
        created__day=today.day,
        goal=goal,
    )


def get_meal_day_goal_query(user, meal):
    today = date.today()

    return DayMeal.objects.filter(
        creator=user,
        created__year=today.year,
        created__month=today.month,
        created__day=today.day,
        meal=meal,
    )


def get_current_calories(user):
    meals = get_user_day_meals(user)
    return sum(filter(None, [get_food_calories(meal) for meal in meals]))


def get_max_calories(user, goal):
    max_calories = user.max_calories
    if goal:
        max_calories = goal.calories
    return max_calories


def get_current_water(user, goal):
    total_water = 0
    goal_query = get_nutritional_day_goal_query(user, goal)
    if goal_query.exists():
        day_goal = goal_query.first()
        total_water = day_goal.water
    return total_water


def get_max_water(goal):
    water = 0
    if goal:
        return goal.water
    return water