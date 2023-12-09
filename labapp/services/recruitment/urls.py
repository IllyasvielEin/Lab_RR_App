from django.urls import path
from . import views

urlpatterns = [
    path('get_recrus', views.get_all_recrus, name='api.get_recrus'),
    path('add_recrus', views.add_recrus, name='api.get_my_apply'),
    path('my_apply', views.get_my_apply, name='api.get_my_apply')
]