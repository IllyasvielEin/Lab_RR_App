from django.urls import reverse
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

from labapp.models import Recruitment, Application, Laboratory
from labapp.models.actions.recruitment import RecruitmentForm


@require_GET
def get_all_recrus(request):
    recrus = Recruitment.objects.all()
    data = list(recrus.values())
    return JsonResponse(data, safe=False)

@require_GET
def get_all_not_expired_recrus(request):
    not_expired_recrus = [recru for recru in Recruitment.objects.all() if not recru.is_expired()]
    return JsonResponse(not_expired_recrus, safe=False)


@require_POST
def add_recrus(request):
    form = RecruitmentForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Recruitment')
    else:
        messages.error(request, form.errors)

    return redirect(reverse('main.index'))


@require_GET
def get_my_apply(request):
    user = request.user
    recrus = Application.objects.filter(user=user)
    data = list(recrus.values())
    return JsonResponse(data, safe=False)


@require_GET
def get_lab_apply(request):
    return None
