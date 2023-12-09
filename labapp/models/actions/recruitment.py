from enum import Enum
from django.db import models
from django.utils import timezone
from django import forms
from django.utils.translation import gettext_lazy as _

from labapp.models.lab.labinfo import Laboratory

class Recruitment(models.Model):
    class Meta:
        app_label = 'labapp'

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))

    last_modified = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Status(models.TextChoices):
        ONGOING = "Ongoing"
        END = "Ended"
    state = models.CharField(max_length=10, choices=Status, default=Status.ONGOING)

    lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE, verbose_name='实验室')

    title = models.CharField(max_length=20, blank=False, verbose_name='招新简述')

    content = models.CharField(max_length=255, blank=False, verbose_name='具体招新内容')

    requirements = models.CharField(max_length=255, blank=False, verbose_name='招新要求')

    recruitment_start_date = models.DateField(blank=False, verbose_name='招新开始时间')

    recruitment_end_date = models.DateField(blank=False, verbose_name='招新结束时间')

    location = models.CharField(max_length=100, verbose_name='招新位置')

    def __str__(self):
        return f"Recruitment for {self.lab.name}"

    def is_expired(self):
        return self.recruitment_end_date < timezone.now().date()

class RecruitmentForm(forms.ModelForm):

    class Meta:
        model = Recruitment
        fields = ['lab', 'title', 'content', 'requirements', 'recruitment_start_date', 'recruitment_end_date', 'location']
        labels = {
            'lab': _('实验室'),
            'title': _('标题'),
            'content': _('具体招新内容'),
            'requirements': _('招新要求'),
            'recruitment_start_date': _('招新开始时间'),
            'recruitment_end_date': _('招新结束时间'),
            'location': _('招新位置'),
        }

    recruitment_start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    recruitment_end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

