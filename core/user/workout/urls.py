from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.UserWorkoutView.as_view()),
    re_path(r'^save/split$', views.UserWorkoutSplitView.as_view()),
]