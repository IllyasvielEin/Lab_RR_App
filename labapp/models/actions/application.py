from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..user import User
from labapp.models.lab.labinfo import Laboratory


class Application(models.Model):
    class Meta:
        app_label = 'labapp'

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))

    last_modified = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='申请人')

    lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE, verbose_name='意向实验室')

    class AppStatus(models.TextChoices):
        APPLIED = 'AP', _('Applied')
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
