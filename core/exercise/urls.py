from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.ExerciseView.as_view()),
    re_path(r'^all$', views.ExercisesAllView.as_view()),
    re_path(r'^types$', views.ExerciseTypesView.as_view()),
    re_path(r'^equipments$', views.ExerciseEquipmentsView.as_view()),
    re_path(r'^muscular-groups$', views.MuscleGroupsView.as_view()),
]