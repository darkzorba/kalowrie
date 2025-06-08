from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^$', views.UserDietView.as_view()),
    re_path(r'^get/cards$', views.ProgressCardsView.as_view()),
    re_path(r'^meal$', views.UserMealView.as_view())
]