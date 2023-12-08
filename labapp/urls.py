from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='main.index'),
    # path('test/', include('labapp.services.test.urls')),
    path('auth/', include('labapp.services.auth.urls')),
    # 其他URL模式和视图函数的映射
]