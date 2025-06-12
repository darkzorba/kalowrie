from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView

import fn.user.user


# Create your views here.



class CreateUserView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]


    def post(self, *args, **kwargs):
        email = self.request.data.get('email')
        password = self.request.data.get('password')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        birth_date = self.request.data.get('birth_date')

        response = fn.user.user.User().create_user(email=email, first_name=first_name, last_name=last_name,
                                                 birth_date=birth_date, password=password)

        return JsonResponse(response, safe=False, status=response['status_code'])