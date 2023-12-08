from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as gl

from labapp.models.lab.labinfo import Laboratory

class Recruitment(models.Model):
    class Meta:
        app_label = 'labapp'

    class Status(models.TextChoices):
        ONGOING = "Ongoing"
        END = "Ended"
    state = models.CharField(max_length=10, choices=Status, default=Status.ONGOING)

    lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE)

    content = models.CharField(max_length=255, blank=False)

    date = models.DateField()

    time = models.CharField(max_length=50)

    requirements = models.CharField(max_length=255, blank=False, verbose_name='招新要求')

    recruitment_start_date = models.DateField(blank=False, verbose_name='招新开始时间')

    recruitment_end_date = models.DateField(blank=False, verbose_name='招新结束时间')

    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Recruitment for {self.lab.name} - {self.date}"
