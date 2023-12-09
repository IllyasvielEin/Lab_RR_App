from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='main.index'),
    # path('test/', include('labapp.services.test.urls')),
    path('auth/', include('labapp.services.auth.urls')),
    path('api/', include('labapp.services.api.urls')),
    path('page/', include('labapp.services.page.urls'))
]