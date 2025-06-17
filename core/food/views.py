from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from fn.diet.food import Food

# Create your views here.




class FoodAllView(APIView):
    def get(self, *args, **kwargs):

        response = Food().get_all_foods()


        return JsonResponse(response, safe=False, status=response['status_code'])




class CreateFoodView(APIView):
    def post(self, *args, **kwargs):
        grams_per_unit = self.request.data.get('grams_per_unit')
        food_name = self.request.data.get('food_name')
        quantity = self.request.data.get('quantity')
        carbs_g = self.request.data.get('carbs_g')
        proteins_g = self.request.data.get('proteins_g')
        fats_g = self.request.data.get('fats_g')
        calories = self.request.data.get('calories')

        response = Food().create_food(name=food_name, quantity=quantity, carbs_g=carbs_g,proteins_g=proteins_g,
                                      fats_g=fats_g,calories=calories, grams_per_unit=grams_per_unit)

        return JsonResponse(response, safe=False, status=response['status_code'])


class CategoriesAllView(APIView):
    def get(self, *args, **kwargs):

        response = Food().get_all_categories()

        return JsonResponse(response, safe=False, status=response['status_code'])