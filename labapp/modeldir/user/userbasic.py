from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserBasicManager(BaseUserManager):
    def create_user(self, username, email, student_id, password=None):

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            student_id=student_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, student_id, password=None):
        user = self.create_user(
            email=email,
            username=username,
            student_id=student_id,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserBasic(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, null=False, verbose_name='用户名')
    student_id = models.CharField(max_length=10, null=False, verbose_name='学号')
    password = models.CharField(max_length=100, null=False, verbose_name='密码')
    email = models.CharField(max_length=50, null=False, verbose_name='邮箱')
    is_admin = models.BooleanField(default=False, verbose_name='是否管理员')

    objects = UserBasicManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'student_id', 'password']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
