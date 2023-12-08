from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name='test_index'),
    # 其他URL模式和视图函数的映射
]