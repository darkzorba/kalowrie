from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from fn.team.team import Team

# Create your views here.





class TeamStudentView(APIView):

    def get(self, *args, **kwargs):

        student_id = self.request.GET.get('student_id')
        team_id = self.request.user.team_id

        response = Team(team_id).get_student(student_id)

        return JsonResponse(response, safe=False, status=response['status_code'])



    def post(self, *args, **kwargs):
        height = self.request.data.get('height')
        weight = self.request.data.get('weight')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        email = self.request.data.get('email')
        gender = self.request.data.get('gender')
        age = self.request.data.get('age')
        password = self.request.data.get('password')
        birth_date = self.request.data.get('birth_date')

        team_id = self.request.user.team_id

        response = Team(team_id).save_student(height=height, weight=weight, first_name=first_name, last_name=last_name,
                                       email=email, gender=gender, age=age, password=password, birth_date=birth_date)

        return JsonResponse(response, safe=False, status=response['status_code'])




class TeamAllStudentView(APIView):
    def get(self, *args, **kwargs):

        team_id = self.request.user.team_id

        response = Team(team_id).get_all_students()

        return JsonResponse(response, safe=False, status=response['status_code'])