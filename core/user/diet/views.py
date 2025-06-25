from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
import json
from fn.diet.diet import Diet
from fn.diet.meal import Meal
from fn.diet.food import Food
# Create your views here.



class UserDietView(APIView):
    def get(self, *args, **kwargs):
        user_id = self.request.GET.get('student_id') or self.request.user.id

        response = Diet(user_id).get_user_diet()


        return JsonResponse(response, safe=False, status=response['status_code'])


    def post(self, *args, **kwargs):
        meals_list = self.request.data.get('meals')
        user_id = self.request.data.get('student_id') or self.request.user.id
        total_carbs = self.request.data.get('carbs_g')
        total_proteins = self.request.data.get('proteins_g')
        total_fats = self.request.data.get('fats_g')
        diet_id = self.request.data.get('diet_id')
        total_calories = self.request.data.get('total_kcals')

        response = Diet(user_id, diet_id).create_diet(meals_list=meals_list, total_carbs=total_carbs,
                                             total_fats=total_fats, total_proteins=total_proteins,
                                             total_calories=total_calories)

        return JsonResponse(response, safe=False, status=response['status_code'])

    def delete(self, *args, **kwargs):

        user_id = self.request.data.get('student_id') or self.request.user.id

        response = Diet(user_id).disable_diet()

        return JsonResponse(response, safe=False, status=response['status_code'])


class ProgressCardsView(APIView):
    def get(self, *args, **kwargs):
        date = self.request.GET.get('date')
        user_id = self.request.user.id

        response = Diet(user_id).get_progress_cards(date)

        return JsonResponse(response, safe=False, status=response['status_code'])


class ProgressGraphView(APIView):
    def get(self, *args, **kwargs):
        date = self.request.GET.get('date')
        user_id = self.request.user.id

        response = Diet(user_id).get_progress_graphics(date)

        return JsonResponse(response, safe=False, status=response['status_code'])


class UserMealView(APIView):
    def post(self, *args, **kwargs):
        user_id = self.request.user.id
        name = self.request.data.get('name')
        meal_time = self.request.data.get('meal_time')
        meal_date = self.request.data.get('meal_date')
        total_kcals = self.request.data.get('total_kcals')
        total_proteins = self.request.data.get('total_proteins')
        total_carbs = self.request.data.get('total_carbs')
        total_fats = self.request.data.get('total_fats')
        diet_id = self.request.data.get('diet_id')
        list_ingredients = self.request.data.get('list_ingredients')

        response = Meal(user_id, diet_id).save_meal(name=name, meal_time=meal_time, meal_date=meal_date, total_kcals=total_kcals,
                                       total_proteins=total_proteins,total_carbs=total_carbs, total_fats=total_fats,
                                                    list_ingredients=list_ingredients)

        return JsonResponse(response, safe=False, status=response['status_code'])



