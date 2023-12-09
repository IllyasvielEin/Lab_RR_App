import logging
from django.shortcuts import render

from labapp.models.user.userbasic import RegistrationForm, LoginForm, UserBasic

logger = logging.getLogger('labapp')


def index(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        perm = user.is_superuser or user.is_staff
        if not perm:
            try:
                profile = UserBasic.objects.get(user=user)
                perm = profile.has_perm()
            except (KeyError, UserBasic.DoesNotExist):
                perm = False
    else:
        perm = False

    # logger.info(f"perm: {perm}")

    if user:
        # logger.info("Has user logged in")
        context = {
            'user': user,
            'has_perm': perm
        }
        return render(request, 'labapp/index.html', context)

    # logger.info("No user logged in")
    login_form = LoginForm()
    register_form = RegistrationForm()
    context = {
        'login_form': login_form,
        'register_form': register_form,
    }
    return render(request, 'labapp/login_index.html', context)
