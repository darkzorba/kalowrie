from django.urls import re_path, include

from . import views

urlpatterns = [
    re_path(r'^diet/', include('core.user.diet.urls')),
    re_path(r'^create$', views.CreateUserView.as_view()),
]