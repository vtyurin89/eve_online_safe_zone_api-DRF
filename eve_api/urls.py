from django.urls import path

from .views import *

urlpatterns = [
    path('api/v1/safe_systems/random/', get_random_safe_system),
]