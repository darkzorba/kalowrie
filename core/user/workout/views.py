import datetime

from django.http import JsonResponse
from datetime import date
from datetime import timedelta
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

        response = Workout(user_id=user_id, workout_id=workout_id).save_workout(week_day=week_day,
                                                         exercises_list=exercises_list, name=name)

        return JsonResponse(response, safe=False, status=response['status_code'])

    def delete(self, *args, **kwargs):
        workout_id = self.request.data.get('workout_id')
        user_id = self.request.data.get('student_id') or self.request.user.id

        response = Workout(user_id=user_id, workout_id=workout_id).disable_workout()

        return JsonResponse(response, safe=False, status=response['status_code'])




class UserWorkoutSplitView(APIView):
    def post(self, *args, **kwargs):
        user_id = self.request.data.get('student_id') or self.request.user.id
        workout_list = self.request.data.get('workouts')

        response = Workout(user_id=user_id).save_workout_split(workout_list)

        return JsonResponse(response, safe=False, status=response['status_code'])


class UserWorkoutSessionView(APIView):
    def post(self, *args, **kwargs):
        user_id = self.request.user.id
        workout_id = self.request.data.get('workout_id')
        session_id = self.request.data.get('session_id')
        total_kgs = self.request.data.get('total_kgs')
        exercises_list = self.request.data.get('exercises_list')
        is_finished = True if self.request.data.get('is_finished') else False

        response = Workout(user_id=user_id, workout_id=workout_id).manage_session(session_id=session_id,
                                                           total_kgs=total_kgs, exercises_list=exercises_list,
                                                                                  is_finished=is_finished)

        return JsonResponse(response, safe=False, status=response['status_code'])



class WorkoutPreviousSetView(APIView):
    def get(self, *args, **kwargs):
        user_id = self.request.user.id
        workout_id = self.request.GET.get('workout_id')

        response = Workout(user_id=user_id, workout_id=workout_id).get_previous_session()

        return JsonResponse(response, safe=False, status=response['status_code'])


class UserWorkoutEvolutionView(APIView):
    def get(self, *args, **kwargs):
        user_id = self.request.user.id
        workout_id = self.request.GET.get('workout_id')
        dat_start = self.request.GET.get('date_start', date.today() - timedelta(days=7))
        dat_end = self.request.GET.get('date_end', date.today())

        response = Workout(user_id=user_id, workout_id=workout_id).get_workout_exercise_evolution(dat_start=dat_start,
                                                                                                  dat_end=dat_end)

        return JsonResponse(response, safe=False, status=response['status_code'])


class UserLastWorkoutsView(APIView):
    def get(self, *args, **kwargs):

        user_id = self.request.user.id

        response = Workout(user_id=user_id).get_last_workouts(days=7)

        return JsonResponse(response, safe=False, status=response['status_code'])