from django.urls import path
from . import views

urlpatterns = [
    path('get_labs', views.get_all_labs, name='api.get_labs'),
    path('add_lab', views.add_lab, name='api.add_lab'),
    path('view_lab/<int:lab_id>', views.view_lab, name='api.view_lab'),
    path('edit_lab/<int:lab_id>', views.edit_lab, name='api.edit_lab'),
    path('update_lab/<int:lab_id>', views.update_lab, name='api.update_lab'),
    path('delete_lab/<int:lab_id>', views.delete_lab, name='api.delete_lab'),
    path('get_labs_for_manage', views.get_labs_for_manage, name='api.get_labs_for_manage')
]