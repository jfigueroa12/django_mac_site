from django.urls import path
from .views import get_info


urlpatterns = [
    path('', get_info, name='info')
]
