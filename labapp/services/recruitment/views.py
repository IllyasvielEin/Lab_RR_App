import logging

from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from labapp.models import Recruitment, Application, Laboratory
from labapp.models.actions.application import ApplicationForm, NewApplicationForm
from labapp.models.actions.recruitment import RecruitmentForm

logger = logging.getLogger(__name__)


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
def add_recru(request):
    form = RecruitmentForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Add recruitment ok')
    else:
        messages.error(request, form.errors)

    return redirect(reverse('main.index'))


def view_recru(request, recru_id: int):
    user = request.user
    recru = Recruitment.objects.get(id=recru_id)
    context = {
        'recruitment': recru,
        'user': user,
    }
    return render(request, 'labapp/recruitment.html', context)


def edit_recru(request, recru_id: int):
    recru = get_object_or_404(Recruitment, id=recru_id)
    form = RecruitmentForm(
        instance=recru,
        initial={
            'state_date': recru.start_date,
            'end_date': recru.end_date,
        }
    )
    context = {
        'form': form,
        'target': reverse('api.update_recru', kwargs={'recru_id': recru_id})
    }
    return render(request, 'labapp/add_sth.html', context)


def update_recru(request, recru_id: int):
    instance = get_object_or_404(Recruitment, id=recru_id)
    form = RecruitmentForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Update recruitment ok')
    else:
        messages.error(request, f'{form.errors}')
    return redirect(reverse('main.index'))


def view_lab_recrus(request, lab_id: int):
    lab = get_object_or_404(Laboratory, id=lab_id)
    recrus = Recruitment.objects.filter(lab=lab)
    context = {
        'lab': lab,
        'recruitments': recrus,
    }
    return render(request, 'labapp/recruitment_list.html', context)


def delete_recru(request, recru_id: int):
    recru = get_object_or_404(Recruitment, id=recru_id)
    lab = Laboratory.objects.get(id=recru.lab.id)

    recru.state = recru.Status.CANCEL
    recru.save()

    return redirect('main.index')
