from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from fn.workout.exercise import Exercise

# Create your views here.




class ExercisesAllView(APIView):
    def get(self, *args, **kwargs):
        team_id = self.request.user.team_id

        response = Exercise().get_all_exercises(team_id)

        return JsonResponse(response, safe=False, status=response['status_code'])