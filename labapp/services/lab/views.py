from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from labapp.models import Laboratory
from labapp.models.lab.labinfo import LabForm


def get_all_labs(request):
    labs = Laboratory.objects.all()
    data = list(labs.values())
    return JsonResponse(data, safe=False)


def add_lab(request):
    user = request.user
    lab = LabForm(request.POST)
    if lab.is_valid():
        messages.success(request, 'Add success')
        instance = lab.save(commit=False)
        instance.supervisor = user
        instance.save()
    else:
        messages.error(request, f'Add error: {lab.errors}')

    return redirect(reverse('page.add_lab'))


def get_labs_for_manage(request):
    user = request.user
    labs = Laboratory.objects.filter(supervisor=user)
    data = list(labs.values())
    return JsonResponse(data, safe=False)


def view_lab(request, lab_id: int):
    user = request.user
    lab = get_object_or_404(Laboratory, id=lab_id)

    context = {
        'lab': lab,
        'user': user
    }
    return render(request, 'labapp/lab.html', context)


def edit_lab(request, lab_id: int):
    user = request.user
    lab = Laboratory.objects.get(id=lab_id)
    form = LabForm(instance=lab)

    context = {
        'user': user,
        'form': form,
        'target': reverse('api.update_lab', kwargs={'lab_id': lab_id}),
    }

    return render(request, 'labapp/add_sth.html', context)


def delete_lab(request, lab_id: int):
    return None


def update_lab(request, lab_id: int):
    instance = Laboratory.objects.get(id=lab_id)
    form = LabForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Update success')

    return redirect('api.edit_lab', lab_id=lab_id)
