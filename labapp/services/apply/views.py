import io
import urllib
import base64
import logging
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

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


def view_apply_chart(request, recru_id: int):
    recruitment = get_object_or_404(Recruitment, id=recru_id)
    lab = recruitment.lab

    untreated_applies = Application.objects.filter(recruitment=recruitment, status=Application.AppStatus.UNDER_REVIEW)
    approve_applies = Application.objects.filter(recruitment=recruitment, status=Application.AppStatus.APPROVE)
    reject_applies = Application.objects.filter(recruitment=recruitment, status=Application.AppStatus.REJECT)

    a_count = untreated_applies.count()
    b_count = approve_applies.count()
    c_count = reject_applies.count()
    sum = a_count + b_count + c_count

    # 生成柱状图
    labels = ['测试', 'Under Review', 'Approved', 'Rejected']
    values = [sum, a_count, b_count, c_count]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['blue', 'green', 'red'])
    plt.xlabel('Application Status')
    plt.ylabel('Number of Applications')
    plt.title('Applications Status Distribution')

    # 将图表转换成数据流
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    context = {
        'lab': lab,
        'image_base64': image_base64
    }

    return render(request, 'labapp/show_image.html', context)