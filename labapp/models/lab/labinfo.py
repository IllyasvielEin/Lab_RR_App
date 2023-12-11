from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Laboratory(models.Model):
    class Meta:
        app_label = 'labapp'

    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='labs', verbose_name='负责人')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))

    last_modified = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    name = models.CharField(max_length=100, unique=True, blank=False, verbose_name='实验室名称')

    description = models.CharField(max_length=255, blank=False, verbose_name='实验室描述')

    contact_information = models.CharField(max_length=100, blank=False, verbose_name='联系方式')

    location = models.CharField(max_length=100, blank=False, verbose_name='地址')

    def __str__(self):
        return self.name


class LabForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = ['name', 'description', 'contact_information', 'location']
        labels = {
            'name': _('实验室名'),
            'description': _('实验室描述'),
            'contact_information': _('联系方式'),
            'location': _('地址'),
        }
