from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

class Laboratory(models.Model):
    class Meta:
        app_label = 'labapp'

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))

    last_modified = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    name = models.CharField(max_length=100, unique=True, blank=False, verbose_name='实验室名称')

    description = models.CharField(max_length=255, blank=False, verbose_name='实验室描述')

    supervisor = models.CharField(max_length=100, blank=False, verbose_name='指导老师')

    contact_information = models.CharField(max_length=100, blank=False, verbose_name='联系方式')

    location = models.CharField(max_length=100, blank=False, verbose_name='地址')

    def __str__(self):
        return self.name


class LabForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = ['name', 'description', 'supervisor', 'contact_information', 'location']
        labels = {
            'lab': _('实验室'),
            'title': _('标题'),
            'content': _('具体招新内容'),
            'requirements': _('招新要求'),
            'recruitment_start_date': _('招新开始时间'),
            'recruitment_end_date': _('招新结束时间'),
            'location': _('招新位置'),
        }