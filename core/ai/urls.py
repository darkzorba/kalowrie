from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^generate/diet$', views.AIDietView.as_view()),
    re_path(r'^track/macros$', views.TrackCaloriesView.as_view())

]