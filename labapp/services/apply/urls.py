from django.urls import path
from . import views

urlpatterns = [
    path('edit_apply/<int:recru_id>', views.edit_apply, name='api.edit_apply'),
    path('add_apply', views.add_apply, name='api.add_apply'),
    path('my_apply', views.get_my_apply, name='api.get_my_apply'),
    path('view_apply/<int:apply_id>', views.view_apply, name='api.view_apply'),
    path('cancel_apply/<int:apply_id>', views.cancel_apply, name='api.cancel_apply'),
    path('approve_apply/<int:apply_id>', views.approve_apply, name='api.approve_apply'),
    path('reject_apply/<int:apply_id>', views.reject_apply, name='api.reject_apply'),
    path('view_apply_list/<int:recru_id>', views.view_apply_list, name='api.view_apply_list'),
    path('view_apply_chart/<int:recru_id>', views.view_apply_chart, name='api.view_apply_chart')
]