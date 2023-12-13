from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

from labapp.models import User
from labapp.models.actions.recruitment import Recruitment
from labapp.models import Laboratory


class Application(models.Model):
    class Meta:
        app_label = 'labapp'

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))

    last_modified = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name='申请人')

    recruitment = models.ForeignKey(
        Recruitment,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='招新词条'
    )

    class AppStatus(models.TextChoices):
        CANCEL = "CC", _('Cancelled')
        UNDER_REVIEW = 'UR', _('Under Review')
        APPROVE = 'AR', _('Approved')
        REJECT = 'RJ', _('Rejected')

    status = models.CharField(max_length=2, choices=AppStatus, default=AppStatus.UNDER_REVIEW)

    remarks = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.lab.name} Application"


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['remarks']
        labels = {
            'remarks': _('备注')
        }


class NewApplicationForm(forms.ModelForm):
    source_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Application
        fields = ['remarks']
        labels = {
            'remarks': _('备注')
        }
