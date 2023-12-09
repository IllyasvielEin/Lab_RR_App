from django.urls import path, include
from . import views


urlpatterns = [
    path('update_user_details/', views.update_user_details, name='api.update_user_details'),
]
