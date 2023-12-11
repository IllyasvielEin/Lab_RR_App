from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET

from labapp.models.actions.recruitment import RecruitmentForm
from labapp.models.lab.labinfo import LabForm
from labapp.models.user.userdetails import UserDetailsForm, UserDetails


@require_GET
def add_recruitment(request):
    context = {
        'form': RecruitmentForm(),
        'target': reverse('api.add_recru')
    }
    return render(request, 'labapp/add_sth.html', context)

@require_GET
def add_lab(request):
    context = {
        'form': LabForm(),
        'target': reverse('api.add_lab')
    }
    return render(request, 'labapp/add_sth.html', context)


def user_details(request):
    current_user = request.user

    if current_user.is_superuser:
        return redirect('/admin')

    try:
        instance = UserDetails.objects.get(user=current_user)
    except (KeyError, UserDetails.DoesNotExist):
        instance = None
    context = {
        'form': UserDetailsForm(instance=instance),
        'target': reverse('api.update_user_details')
    }
    return render(request, 'labapp/add_sth.html', context)
