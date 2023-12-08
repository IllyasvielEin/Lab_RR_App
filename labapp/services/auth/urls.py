from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.handle_sighup, name='auth.sighup'),
    path('login', views.handle_login, name='auth.login'),
    path('logout', views.handle_logout, name='auth.logout'),
]