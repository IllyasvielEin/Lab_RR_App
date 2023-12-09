from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect

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
