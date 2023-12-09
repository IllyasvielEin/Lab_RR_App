from django.urls import path, include
from . import views


urlpatterns = [
    path('recruitment/', include('labapp.services.recruitment.urls')),
    path('lab/', include('labapp.services.lab.urls')),
    path('user/', include('labapp.services.user.urls'))
]
