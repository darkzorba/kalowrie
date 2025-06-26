from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from fn.workout.exercise import Exercise

# Create your views here.


class ExerciseView(APIView):
    def post(self, *args, **kwargs):
        name = self.request.data.get('name')
        muscular_group_id = self.request.data.get('muscular_group_id')
        exercise_type_id = self.request.data.get('exercise_type_id')
        exercise_equipment_id = self.request.data.get('exercise_equipment_id')
        exercise_photo = self.request.FILES.get('exercise_photo')

        response = Exercise().save_exercise(name=name, muscle_group_id=muscular_group_id, type_id=exercise_type_id,
                                            equipment_id=exercise_equipment_id, image=exercise_photo)

        return JsonResponse(response, safe=False, status=response['status_code'])


class ExercisesAllView(APIView):
    def get(self, *args, **kwargs):
        team_id = self.request.user.team_id

        response = Exercise().get_all_exercises(team_id)

        return JsonResponse(response, safe=False, status=response['status_code'])



class MuscleGroupsView(APIView):
    def get(self, *args, **kwargs):

        response = Exercise().get_muscular_groups()

        return JsonResponse(response, safe=False, status=response['status_code'])


class ExerciseTypesView(APIView):
    def get(self, *args, **kwargs):

        response = Exercise().get_exercise_types()

        return JsonResponse(response, safe=False, status=response['status_code'])


class ExerciseEquipmentsView(APIView):
    def get(self, *args, **kwargs):
        response = Exercise().get_exercise_equipments()
        return JsonResponse(response, safe=False, status=response['status_code'])
