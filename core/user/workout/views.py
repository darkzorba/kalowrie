from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from fn.workout.workout import Workout

# Create your views here.





class UserWorkoutView(APIView):
    def get(self, *args, **kwargs):
        user_id = self.request.GET.get('student_id') or self.request.user.id

        response = Workout(user_id=user_id).get_user_workout_split()

        return JsonResponse(response, safe=False, status=response['status_code'])


    def post(self, *args, **kwargs):
        user_id = self.request.data.get('student_id') or self.request.user.id
        workout_id = self.request.data.get('workout_id')
        week_day = self.request.data.get('day_of_week')
        exercises_list = self.request.data.get('exercises')
        name = self.request.data.get('name')

        response = Workout(user_id=user_id).save_workout(workout_id=workout_id,week_day=week_day,
                                                         exercises_list=exercises_list, name=name)

        return JsonResponse(response, safe=False, status=response['status_code'])

    def delete(self, *args, **kwargs):
        workout_id = self.request.data.get('workout_id')
        user_id = self.request.data.get('student_id') or self.request.user.id

        response = Workout(user_id=user_id).disable_workout(workout_id=workout_id)

        return JsonResponse(response, safe=False, status=response['status_code'])




class UserWorkoutSplitView(APIView):
    def post(self, *args, **kwargs):
        user_id = self.request.data.get('student_id') or self.request.user.id
        workout_list = self.request.data.get('workouts')

        response = Workout(user_id=user_id).save_workout_split(workout_list)

        return JsonResponse(response, safe=False, status=response['status_code'])