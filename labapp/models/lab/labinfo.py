from django.db import models

class Laboratory(models.Model):
    class Meta:
        app_label = 'labapp'

    name = models.CharField(max_length=100, unique=True, blank=False, verbose_name='实验室名称')

    description = models.CharField(max_length=255, blank=False, verbose_name='实验室描述')

    supervisor = models.CharField(max_length=100, blank=False, verbose_name='指导老师')

    contact_information = models.CharField(max_length=100, blank=False, verbose_name='联系方式')

    location = models.CharField(max_length=100, blank=False, verbose_name='地址')

    def __str__(self):
        return self.name
