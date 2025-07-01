from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.UserWorkoutView.as_view()),
    re_path(r'^save/split$', views.UserWorkoutSplitView.as_view()),
    re_path(r'^session$', views.UserWorkoutSessionView.as_view()),
    re_path(r'^session/previous$', views.WorkoutPreviousSetView.as_view()),
    re_path(r'^evolution$', views.UserWorkoutEvolutionView.as_view()),
    re_path(r'^last$', views.UserLastWorkoutsView.as_view()),
]