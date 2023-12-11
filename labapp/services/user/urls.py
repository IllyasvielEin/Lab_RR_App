from django.urls import path, include
from . import views


urlpatterns = [
    path('update_user_details/', views.update_user_details, name='api.update_user_details'),
    path('<int:recru_id>/view_user_details/<int:user_id>', views.view_user_details, name='api.view_user_details'),
]
