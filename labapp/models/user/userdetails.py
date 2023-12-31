from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserDetails(models.Model):
    class Meta:
        app_label = 'labapp'

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))

    last_modified = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')

    name = models.CharField(max_length=100, null=False, verbose_name='真实姓名')

    class GenderType(models.TextChoices):
        MALE = "M"
        FEMALE = "F"
        SECRET = "S"
        OTHER = "O"

    gender = models.CharField(max_length=1, blank=False, choices=GenderType, default=GenderType.SECRET, verbose_name='性别')

    age = models.IntegerField(verbose_name='年龄')

    class MajorType(models.TextChoices):
        COMPUTER_SCIENCE = "CS", "计算机科学与技术"
        SOFTWARE_ENGINEERING = "SE", "软件工程"
        DATA_SCIENCE = "DS", "数据科学"
        INFORMATION_SYSTEMS = "IS", "信息系统"
        NETWORK_ENGINEERING = "NE", "网络工程"
        CYBER_SECURITY = "CSY", "网络安全"
        ARTIFICIAL_INTELLIGENCE = "AI", "人工智能"
        COMPUTER_ENGINEERING = "CE", "计算机工程"
        INFORMATION_SECURITY = "ISY", "信息安全"
        EMBEDDED_SYSTEMS = "ES", "嵌入式开发"
    major = models.CharField(max_length=3, choices=MajorType, blank=False, verbose_name='专业')

    contact = models.CharField(max_length=50, blank=False, verbose_name='联系方式')

    hobbies = models.CharField(max_length=255, verbose_name='爱好')

    is_finish_details = models.BooleanField(default=False, verbose_name='信息填写完毕')

    def __str__(self):
        return self.name


class Project(models.Model):
    class Meta:
        app_label = 'labapp'

    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=20, verbose_name='项目名称')
    responsibilities = models.CharField(max_length=10, verbose_name='项目角色')
    time = models.DateField(verbose_name='项目时间')
    description = models.CharField(max_length=255, verbose_name='项目描述')
    achievement = models.CharField(max_length=100, verbose_name='项目成就')

    def __str__(self):
        return self.name

class Rewards(models.Model):
    class Meta:
        app_label = 'labapp'

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


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['name', 'gender', 'major', 'age', 'contact', 'hobbies']
        labels = {
            'name': _('真实姓名'),
            'gender': _('性别'),
            'major': _('专业'),
            'age': _('年龄'),
            'contact': _('联系方式'),
            'hobbies': _('爱好')
        }
