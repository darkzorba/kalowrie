from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^get/diet$', views.AIDietView.as_view()),

]