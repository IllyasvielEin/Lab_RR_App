from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # 其他URL模式和视图函数的映射
]