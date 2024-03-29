import ast

from django import template

from utils.food import get_nutritional_translated as get_nutritional_translated_util
from utils.nutritional import get_nutrient_value as get_nutrient_value_util
from utils.utils import format_water

register = template.Library()


@register.filter()
def get_nutrient_value(meal_food, name):
    return get_nutrient_value_util(meal_food, name)


@register.simple_tag
def create_dict(str_dict):
    return ast.literal_eval(str_dict)


@register.filter()
def format_nutrient(nutrient_value, nutrient_name):
    nutrients_info = {
        'calories': 'kcal', 'carbohydrate': 'g', 'protein': 'g', 'fat': 'g',
        'saturated_fat': 'g', 'polyunsaturated_fat': 'g', 'monounsaturated_fat': 'g',
        'trans_fat': 'g', 'cholesterol': 'mg', 'sodium': 'mg', 'potassium': 'mg', 'fiber': 'g',
        'sugar': 'g', 'added_sugars': 'g', 'vitamin_d': 'mg', 'vitamin_a': 'mg', 'vitamin_c': 'mg',
        'calcium': 'mg', 'iron': 'mg',
    }
    if nutrient_name == 'water':
        return format_water(nutrient_value)

    if int(nutrient_value) == 0:
        nutrient_value = 0
    else:
        nutrient_value = f'{nutrient_value:.1f}'

    return f'{nutrient_value}{nutrients_info.get(nutrient_name)}'


@register.filter()
def get_nutritional_translated(value):
    return get_nutritional_translated_util(value)
