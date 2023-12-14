from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_GET

from labapp.models import Application
from labapp.models.user.userdetails import UserDetailsForm


def update_user_details(request):
    form = UserDetailsForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.is_finish_details = True
        instance.save()
        messages.success(request, 'Your details have been changed')
    else:
        messages.error(request, f'{form.errors}')
    return redirect(reverse('page.user_details'))


@require_GET
def view_user_details(request, user_id: int, recru_id: int):
    user = request.user
    target_user = get_object_or_404(User, id=user_id)
    target_apply = Application.objects.get(recruitment_id=recru_id, user_id=target_user)
    context = {
        'recru_id': recru_id,
        'current_user': user,
        'target_user': target_user,
        'apply': target_apply
    }

    return render(request, 'labapp/user_profile.html', context)
