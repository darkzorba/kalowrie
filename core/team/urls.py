from django.urls import re_path
from . import views


urlpatterns = [

    re_path(r'^student$', views.TeamStudentView.as_view()),
    re_path(r'^students/all$', views.TeamAllStudentView.as_view()),
]