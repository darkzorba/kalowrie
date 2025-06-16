from django.db import models

import core.models


# Create your models here.



class UserDiet(core.models.Log):
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, null=True)
    diet_json = models.JSONField(null=True)

    total_kcals = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    proteins_g = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    carbs_g = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    fats_g = models.DecimalField(max_digits=14,decimal_places=2,null=True)

    class Meta:
        db_table = '"public"."user_diet"'


class UserDietMeal(core.models.Log):
    name = models.CharField(max_length=120)
    time = models.TimeField()
    diet = models.ForeignKey('diet.UserDiet', on_delete=models.DO_NOTHING, null=True)
    total_proteins = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    total_fats = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    total_calories = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    total_carbs = models.DecimalField(max_digits=14,decimal_places=2,null=True)


    class Meta:
        db_table = '"public"."user_dietmeal"'


class UserDietMealComponent(core.models.Log):
    diet_meal = models.ForeignKey('diet.UserDietMeal', on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=120)
    total_proteins = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    total_fats = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    total_carbs = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    quantity = models.IntegerField(null=True)
    unit = models.CharField(max_length=120)

    class Meta:
        db_table = '"public"."user_diet_mealcomponent"'


class MealComponentSubstitution(core.models.Log):
    meal_component = models.ForeignKey('diet.UserDietMealComponent', on_delete=models.DO_NOTHING, null=True,
                                       related_name='substitutions_as_main')
    substitution = models.ForeignKey('diet.UserDietMealComponent', on_delete=models.DO_NOTHING, null=True,
                                     related_name='substitutions_as_alternative')

    class Meta:
        db_table = '"public"."meal_component_substitution"'


class UserDailyProgress(core.models.Log):
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, null=True)
    date = models.DateField(null=True)
    total_proteins = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    total_fats = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    total_carbs = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    total_kcals = models.DecimalField(max_digits=14,decimal_places=2,null=True)

    kcals_goal = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    proteins_goal = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    fats_goal = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    carbs_goal = models.DecimalField(max_digits=14,decimal_places=2,null=True)

    diet = models.ForeignKey('diet.UserDiet', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = '"public"."user_dailyprogress"'


class UserMeal(core.models.Log):
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=200, null=True)
    calories = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    proteins_gr = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    fats_gr = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    carbs_gr = models.DecimalField(max_digits=14,decimal_places=2,null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    class Meta:
        db_table = '"public"."user_meal"'


class UserMealIngredient(core.models.Log):
    name = models.CharField(max_length=200, null=True)
    quantity = models.IntegerField(null=True)
    unit = models.CharField(max_length=50, null=True)
    meal = models.ForeignKey('diet.UserMeal', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = '"public"."user_mealingredient"'


class FoodMacro(core.models.Log):
    name = models.CharField(max_length=200, null=True)
    quantity = models.IntegerField(null=True)
    fats_g = models.DecimalField(null=True, max_digits=14, decimal_places=2)
    proteins_g = models.DecimalField(null=True, max_digits=14, decimal_places=2)
    carbs_g = models.DecimalField(null=True, max_digits=14, decimal_places=2)
    category = models.ForeignKey('diet.FoodCategory', on_delete=models.DO_NOTHING, null=True)
    calories = models.DecimalField(null=True, max_digits=14, decimal_places=2)
    grams_per_unit = models.IntegerField(null=True)

    class Meta:
        db_table = '"public"."food_macro"'


class FoodCategory(core.models.Log):
    name = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = '"public"."food_category"'