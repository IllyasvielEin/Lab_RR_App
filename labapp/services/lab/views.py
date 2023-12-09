from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from labapp.models import Laboratory
from labapp.models.lab.labinfo import LabForm


def get_all_labs(request):
    labs = Laboratory.objects.all()
    data = list(labs.values())
    return JsonResponse(data, safe=False)


def add_lab(request):
    lab = LabForm(request.POST)
    if lab.is_valid():
        messages.success(request, 'Add success')
        lab.save()
    else:
        messages.error(request, f'Add error: {lab.errors}')

    return redirect(reverse('page.add_lab'))
