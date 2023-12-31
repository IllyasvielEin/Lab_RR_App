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

from labapp.models.actions import Application, Recruitment
from labapp.models.user import UserDetails
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

    recruitment_list = Application.objects.filter(recruitment=recruitment)

    status_dict = {key[0]: 0 for key in Application.AppStatus.choices}
    major_dict = {key[0]: 0 for key in UserDetails.MajorType.choices}


    # 数据清洗及处理
    for i in recruitment_list:
        status_dict[i.status] += 1
        major_dict[i.user.details.major] += 1

    status_dict = {str(new_key):status_dict[old_key] for old_key, new_key in Application.AppStatus.choices}
    major_dict = {str(new_key):major_dict[old_key] for old_key, new_key in UserDetails.MajorType.choices}

    # 柱状图-处理情况-总数-未处理-已通过-未通过
    plt.figure(figsize=(8, 6))
    plt.bar(status_dict.keys(), status_dict.values())
    plt.xlabel('申请状态')
    plt.ylabel('人数')
    plt.title('申请状态分布')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    application_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.clf()

    # 图-申请人专业分析
    fig, axs = plt.subplots(1, 2, figsize=(15, 5), gridspec_kw={'width_ratios': [2.7, 1]})
    # 子图-柱状图
    axs[0].bar(major_dict.keys(), major_dict.values())
    axs[0].set_xlabel('专业')
    axs[0].set_ylabel('人数')
    axs[0].set_title('申请人专业分布')
    # 子图-饼状图
    major_dict = {key:value for key, value in major_dict.items() if value != 0}
    axs[1].pie(major_dict.values(), labels=major_dict.keys(), autopct='%1.1f%%', startangle=90)
    axs[1].set_title('各专业人数占比')
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    major_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.clf()

    context = {
        'lab': lab,
        'application_chart': application_chart,
        'major_chart': major_chart
    }

    return render(request, 'labapp/show_image.html', context)