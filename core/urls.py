from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    re_path('^login$', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path('^ai/', include('core.ai.urls')),
    re_path(r'^user/', include('core.user.urls')),
    re_path(r'^food/', include('core.food.urls')),
    re_path(r'^team/', include('core.team.urls')),
    re_path(r'^exercise/', include('core.exercise.urls')),
]