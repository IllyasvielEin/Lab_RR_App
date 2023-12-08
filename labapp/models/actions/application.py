from django.db import models
from django.utils.translation import gettext_lazy as _

from ..user import User
from labapp.models.lab.labinfo import Laboratory


class Application(models.Model):
    class Meta:
        app_label = 'labapp'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    application_date = models.DateField(blank=False, auto_now_add=True)

    class AppStatus(models.TextChoices):
        APPLIED = 'AP', _('Applied')
        UNDER_REVIEW = 'UR', _('Under Review')
        APPROVE = 'AR', _('Approved')
        REJECT = 'RJ', _('Rejected')
    status = models.CharField(max_length=2, choices=AppStatus, default=AppStatus.APPLIED)

    remarks = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.lab.name} Application"
