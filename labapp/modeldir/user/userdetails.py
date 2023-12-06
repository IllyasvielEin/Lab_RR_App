from django.db import models
from django.utils.translation import gettext_lazy as _

class UserDetails(models.Model):

    name = models.CharField(max_length=100, null=False, verbose_name='真实姓名')

    class GenderType(models.TextChoices):
        MALE = "M"
        END = "F"
        SECRET = "S"
        OTHER = "O"

    gender = models.CharField(max_length=1, null=False, choices=GenderType, default=GenderType.SECRET, verbose_name='性别')

    age = models.IntegerField(verbose_name='年龄')

    major = models.CharField(max_length=100, null=False, verbose_name='专业')

    student_id = models.CharField(max_length=20, null=False, verbose_name='学号')

    contact = models.CharField(max_length=50, null=False, verbose_name='联系方式')

    hobbies = models.CharField(max_length=255, verbose_name='爱好')

    special_skills = models.CharField(max_length=255, verbose_name='特长')

    social_practice = models.CharField(max_length=255, verbose_name='社会实践')

    def __str__(self):
        return self.name


class Project(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=20, verbose_name='项目名称')
    responsibilities = models.CharField(max_length=10, verbose_name='项目角色')
    time = models.DateField(verbose_name='项目时间')
    description = models.CharField(max_length=255, verbose_name='项目描述')
    achievement = models.CharField(max_length=100, verbose_name='项目成就')

    def __str__(self):
        return self.name

class Rewards(models.Model):
    users = models.ManyToManyField(UserDetails, related_name='rewards')

    name = models.CharField(max_length=100, verbose_name='获奖名称')

    class GenderType(models.IntegerChoices):
        GRAND = 0, _("Grand Prize")
        FIRST = 1, _("First Prize")
        SECOND = 2, _("Second Prize")
        THIRD = 3, _("Third Prize")
        OTHER = 4, _("Other")

    level = models.IntegerField(choices=GenderType, verbose_name='获奖等级')

    time = models.DateField(verbose_name='获奖时间')

    def __str__(self):
        return self.name
