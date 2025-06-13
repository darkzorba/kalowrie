from django.db import models

import core.models


# Create your models here.



class UserDiet(core.models.Log):
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, null=True)
    diet_json = models.JSONField(null=True)

    total_kcals = models.IntegerField(null=True)
    proteins_g = models.IntegerField(null=True)
    carbs_g = models.IntegerField(null=True)
    fats_g = models.IntegerField(null=True)

    class Meta:
        db_table = '"public"."user_diet"'


class UserDailyProgress(core.models.Log):
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, null=True)
    date = models.DateField(null=True)
    total_proteins = models.IntegerField(null=True)
    total_fats = models.IntegerField(null=True)
    total_carbs = models.IntegerField(null=True)
    total_kcals = models.IntegerField(null=True)

    kcals_goal = models.IntegerField(null=True)
    proteins_goal = models.IntegerField(null=True)
    fats_goal = models.IntegerField(null=True)
    carbs_goal = models.IntegerField(null=True)

    diet = models.ForeignKey('diet.UserDiet', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = '"public"."user_dailyprogress"'


class UserMeal(core.models.Log):
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=200, null=True)
    calories = models.IntegerField(null=True)
    proteins_gr = models.IntegerField(null=True)
    fats_gr = models.IntegerField(null=True)
    carbs_gr = models.IntegerField(null=True)
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

    class Meta:
        db_table = '"public"."food_macro"'


class FoodCategory(core.models.Log):
    name = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = '"public"."food_category"'