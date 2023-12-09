from django.urls import path, include
from . import views


urlpatterns = [
    path('add_recruitment/', view=views.add_recruitment, name='page.add_recruitment'),
    path('add_lab/', view=views.add_lab, name='page.add_lab'),
    path('user_details/', view=views.user_details, name='page.user_details')
]
