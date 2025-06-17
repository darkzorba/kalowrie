from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^all$', views.FoodAllView.as_view()),
    re_path(r'^add$', views.CreateFoodView.as_view()),
    re_path(r'^categories/all$', views.CategoriesAllView.as_view()),
]