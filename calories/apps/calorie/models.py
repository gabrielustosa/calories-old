from django.db import models

from calories.apps.core.models import CreatorBase, TimeStampedBase


class Food(models.Model):
    food_id = models.PositiveBigIntegerField()
    food_name = models.CharField(max_length=100)
    calories = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    carbohydrate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    protein = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    fat = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    saturated_fat = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    polyunsaturated_fat = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    monounsaturated_fat = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    trans_fat = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    cholesterol = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sodium = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    potassium = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    fiber = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sugar = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    added_sugars = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    vitamin_d = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    vitamin_a = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    vitamin_c = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    calcium = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    iron = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    measurement_description = models.CharField(max_length=100)
    number_of_units = models.DecimalField(max_digits=15, decimal_places=2)


class FoodMeal(models.Model):
    serving_amount = models.DecimalField(max_digits=10, decimal_places=1)
    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name='measurements'
    )


class Meal(CreatorBase):
    ICONS = (
        ('Apple', 'Apple'),
        ('Carrot', 'Carrot'),
        ('Egg', 'Egg'),
        ('Lemon', 'Lemon'),
        ('Bacon', 'Bacon'),
        ('Chicken', 'Chicken'),
        ('Cheese', 'Cheese'),
        ('Cookie', 'Cookie'),
        ('Fish', 'Fish'),
        ('Burger', 'Burger'),
    )
    name = models.CharField(max_length=100)
    time = models.TimeField()
    icon = models.CharField(max_length=100, choices=ICONS)

    def get_icon(self):
        icon_class = ''

        if self.icon == 'Apple':
            icon_class = 'fa-solid fa-apple-whole'
        elif self.icon == 'Carrot':
            icon_class = 'fa-solid fa-carrot'
        elif self.icon == 'Egg':
            icon_class = 'bi bi-egg-fried'
        elif self.icon == 'Lemon':
            icon_class = 'fa-solid fa-lemon'
        elif self.icon == 'Bacon':
            icon_class = 'fa-solid fa-bacon'
        elif self.icon == 'Chicken':
            icon_class = 'fa-solid fa-drumstick-bite'
        elif self.icon == 'Cheese':
            icon_class = 'fa-solid fa-cheese'
        elif self.icon == 'Cookie':
            icon_class = 'fa-solid fa-cookie'
        elif self.icon == 'Fish':
            icon_class = 'fa-solid fa-fish-fins'
        elif self.icon == 'Burger':
            icon_class = 'fa-solid fa-burger'

        return f'<i class="{icon_class}"></i>'


class DayMeal(CreatorBase, TimeStampedBase):
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE
    )
    foods = models.ManyToManyField(FoodMeal)
