from django.urls import path
from . import views

urlpatterns = [
    path('get_recrus', views.get_all_recrus, name='api.get_recrus'),
    path('view_recru/<int:recru_id>', views.view_recru, name='api.view_recru'),
    path('view_lab_recrus/<int:lab_id>', views.view_lab_recrus, name='api.view_lab_recrus'),
    path('add_recru', views.add_recru, name='api.add_recru'),
    path('edit_recru/<int:recru_id>', views.edit_recru, name='api.edit_recru'),
    path('update_recru/<int:recru_id>', views.update_recru, name='api.update_recru'),
]