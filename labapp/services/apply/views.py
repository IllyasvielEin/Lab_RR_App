import logging

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from labapp.models import Application, Recruitment
from labapp.models.actions.application import ApplicationForm, NewApplicationForm


logger = logging.getLogger(__name__)

def approve_apply(request, apply_id: int):
    apply = get_object_or_404(Application, id=apply_id)
    apply.status = apply.AppStatus.APPROVE
    apply.save()
    messages.success(request, 'Apply success')
    return redirect('api.view_apply_list', apply.recruitment.lab.id)


def reject_apply(request, apply_id: int):
    apply = get_object_or_404(Application, id=apply_id)
    apply.status = apply.AppStatus.REJECT
    apply.save()
    messages.success(request, 'Apply success')
    return redirect('api.view_apply_list', apply.recruitment.lab.id)


def view_apply(request, apply_id: int):
    user = request.user
    apply = get_object_or_404(Application, id=apply_id)
    context = {
        'user': user,
        'apply': apply
    }
    return render(request, 'labapp/view_apply.html', context)


def cancel_apply(request, apply_id: int):
    user = request.user
    apply = get_object_or_404(Application, id=apply_id)
    if user.id != apply.user.id:
        messages.error(request, 'You do not have permission to cancel')
        return redirect(reverse('main.index'))

    apply.status = apply.AppStatus.CANCEL
    apply.save()
    messages.success(request, 'Cancel success')

    return redirect(reverse('api.view_apply', args=(apply.id,)))

@require_GET
def edit_apply(request, recru_id: int):
    user = request.user

    ok = True
    try:
        details_instance = user.details
        ok = details_instance.is_finish_details
    except Exception as e:
        ok = False

    if not ok:
        messages.error(request, '点击右上角用户名处完善自身资料！')
        return redirect(reverse('main.index'))

    form = ApplicationForm()
    context = {
        'form': form,
        'source_id': recru_id,
        'target': reverse('api.add_apply'),
    }
    return render(request, 'labapp/add_sth.html', context)


def add_apply(request):
    form = NewApplicationForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        source_id = form.cleaned_data['source_id']
        logger.info(f'source: {source_id}')
        source_recruitment = Recruitment.objects.get(id=source_id)
        instance.recruitment = source_recruitment
        instance.save()
        messages.success(request, 'Apply ok')
    else:
        messages.error(request, f'{form.errors}')
    return redirect(reverse('main.index'))

@require_GET
def get_my_apply(request):
    user = request.user
    applies = Application.objects.filter(user=user)
    data = []
    for app in applies:
        app_data = {
            'lab_name': app.lab.name,
            'status': app.get_status_display()  # 添加标签值到字典中
        }
        data.append(app_data)
    return JsonResponse(data, safe=False)


@require_GET
def get_lab_apply(request):
    return None


def view_apply_list(request, recru_id: int):
    recruitment = get_object_or_404(Recruitment, id=recru_id)
    applications = Application.objects.filter(recruitment=recruitment)
    if applications.count() == 0:
        applications = None

    untreated_applies = Application.objects.filter(recruitment=recruitment, status=Application.AppStatus.UNDER_REVIEW)
    approve_applies = Application.objects.filter(recruitment=recruitment, status=Application.AppStatus.APPROVE)
    reject_applies = Application.objects.filter(recruitment=recruitment, status=Application.AppStatus.REJECT)

    context = {
        'lab': recruitment.lab,
        'a_applies': untreated_applies,
        'b_applies': approve_applies,
        'c_applies': reject_applies,
    }
    return render(request, 'labapp/lab_applies.html', context)
