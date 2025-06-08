from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
import json
from fn.diet.diet import Diet
from fn.diet.meal import Meal
# Create your views here.



class UserDietView(APIView):
    def get(self, *args, **kwargs):
        user_id = self.request.user.id

        response = Diet(user_id).get_user_diet()


        return JsonResponse(response, safe=False, status=response['status_code'])



    def post(self, *args, **kwargs):
        user_id = self.request.user.id
        diet_dict = self.request.data.get('diet_json')

        response = Diet(user_id).save_diet(diet_dict)

        return JsonResponse(response, safe=False, status=response['status_code'])



class ProgressCardsView(APIView):
    def get(self, *args, **kwargs):
        date = self.request.GET.get('date')
        user_id = self.request.user.id

        response = Diet(user_id).get_progress_cards(date)

        return JsonResponse(response, safe=False, status=response['status_code'])



class UserMealView(APIView):
    def post(self, *args, **kwargs):
        user_id = self.request.user.id
        name = self.request.GET.get('name')
        meal_time = self.request.GET.get('meal_time')
        meal_date = self.request.GET.get('meal_date')
        total_kcals = self.request.GET.get('total_kcals')
        total_proteins = self.request.GET.get('total_proteins')
        total_carbs = self.request.GET.get('total_carbs')
        total_fats = self.request.GET.get('total_carbs')
        diet_id = self.request.GET.get('diet_id')

        response = Meal(user_id, diet_id).save_meal(name=name, meal_time=meal_time, meal_date=meal_date, total_kcals=total_kcals,
                                       total_proteins=total_proteins,total_carbs=total_carbs, total_fats=total_fats)

        return JsonResponse(response, safe=False, status=response['status_code'])