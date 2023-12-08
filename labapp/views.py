import logging
from django.shortcuts import render

from labapp.models.user.userbasic import RegistrationForm, LoginForm


logger = logging.getLogger('labapp')


def index(request, user=None):
    if user is None:
        user = request.user if request.user.is_authenticated else None

    if user:
        logger.info("Has user logged in")
        context = {
            'user': user
        }
        return render(request, 'labapp/index.html', context)

    logger.info("No user logged in")
    login_form = LoginForm()
    register_form = RegistrationForm()
    context = {
        'login_form': login_form,
        'register_form': register_form
    }
    return render(request, 'labapp/login_index.html', context)
