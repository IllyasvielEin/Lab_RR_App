from django.urls import path
from . import views

urlpatterns = [
    path('get_labs', views.get_all_labs, name='api.get_labs'),
    path('add_labs', views.add_lab, name='api.add_lab'),
    path('get_labs_for_manage', views.get_labs_for_manage, name='api.get_labs_for_manage')
]