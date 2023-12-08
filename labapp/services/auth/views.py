import logging
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from labapp.models import User
from labapp.models.user.userbasic import RegistrationForm, UserBasic, LoginForm
from django.contrib.auth import login, logout

logger = logging.getLogger(__name__)

@require_POST
def handle_sighup(request):
    form = RegistrationForm(request.POST)
    try:
        if form.is_valid():
            username = form.cleaned_data['username']
            student_id = form.cleaned_data['student_id']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            user = User.objects.create_user(username=username, password=password, email=email)
            user_profile = UserBasic.objects.create(student_id=student_id, user=user)
            user_profile.save()
            messages.success(request, 'Registration successful.')
            login(request, user)
            return redirect(reverse('main.index'), user=user)
        else:
            logger.error(form.errors)
            messages.error(request, f'{form.errors}')
    except Exception as e:
        logger.exception(e)

    return redirect(reverse('main.index'))


@require_POST
def handle_login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        ok = False
        user = User.objects.get(username=username)
        if user:
            if user.check_password(password):
                login(request, user)
                ok = True
                messages.success(request, 'Login success')
        else:
            user_profile = UserBasic.objects.get(student_id=username)
            if user_profile is not None:
                if user_profile.user.check_password(password):
                    login(request, user_profile.user)
                    ok = True
                    messages.success(request, 'Login success')

        if not ok:
            messages.error(request, 'No such username or error password')
    else:
        messages.error(request, 'Internal Server Error.')

    return redirect(reverse('main.index'))


@require_POST
def handle_logout(request):
    logout(request)
    return redirect('main.index')
