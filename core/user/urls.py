from django.urls import re_path, include

urlpatterns = [
    re_path(r'^diet/', include('core.user.diet.urls'))
]