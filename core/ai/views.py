from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

import fn.ai.nutricionist
import fn.ai.tracker

# Create your views here.


class AIDietView(APIView):
    def post(self, *args, **kwargs):
        activity_frequency = self.request.data.get('activity_frequency')
        age = self.request.data.get('age')
        dietary_preferences = self.request.data.get('dietary_preferences')
        dietary_restrictions = self.request.data.get('dietary_restrictions')
        eating_routine = self.request.data.get('eating_routine')
        gender = self.request.data.get('gender')
        height = self.request.data.get('height')
        weight = self.request.data.get('weight')
        diet_type = self.request.data.get('diet_type')

        response = fn.ai.nutricionist.Nutrition().generate_diet(activity_frequency=activity_frequency, age=age,
                                        dietary_preferences=dietary_preferences, dietary_restrictions=dietary_restrictions,
                                        eating_routine=eating_routine, gender=gender, height=height, weight=weight,
                                                                diet_type=diet_type)
        return JsonResponse(response, safe=False, status=response['status_code'])



class TrackCaloriesView(APIView):
    def post(self, *args, **kwargs):
        list_ingredients = self.request.data.get('list_ingredients')
        name = self.request.data.get('name')
        amount = self.request.data.get('amount')
        food_img = self.request.FILES.get('food_img')
        response = fn.ai.tracker.CalorieTracker().track_macros(list_ingredients=list_ingredients, name=name,
                                                               amount=amount, food_img=food_img)

        return JsonResponse(response, safe=False, status=response['status_code'])