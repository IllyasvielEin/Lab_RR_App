import logging
from django.shortcuts import render

from labapp.models import Recruitment, Laboratory, Application
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

    if user:
        all_recrus = Recruitment.objects.all()
        for recru in all_recrus:
            if recru.state == Recruitment.Status.ONGOING and recru.is_expired():
                recru.state = recru.Status.END
                recru.save()
        recrus = Recruitment.objects.filter(state=Recruitment.Status.ONGOING).order_by('-created_at')
        labs = Laboratory.objects.all()
        my_applies = Application.objects.filter(user=user)
        my_labs = None
        if perm:
            my_labs = Laboratory.objects.filter(supervisor=user)
        context = {
            'user': user,
            'has_perm': perm,
            'recruitments': recrus,
            'labs': labs,
            'my_appies': my_applies,
            'my_labs': my_labs
        }
        return render(request, 'labapp/index.html', context)
    else:
        login_form = LoginForm()
        register_form = RegistrationForm()
        context = {
            'login_form': login_form,
            'register_form': register_form,
        }
        return render(request, 'labapp/login_index.html', context)
