from django import forms
from django.db import models
from django.contrib.auth.models import User


class UserBasic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_id = models.CharField(
        max_length=10,
        blank=False,
        verbose_name='学号'
    )

    def __str__(self):
        return self.user.username

class RegistrationForm(forms.Form):

    username = forms.CharField(
        label='Username',
        max_length=20,
        required=True,
        min_length=2,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    student_id = forms.CharField(
        label='Student ID',
        required=True,
        max_length=10,
        min_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username or student_id already existed')
        student_id = cleaned_data['student_id']
        if UserBasic.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError('Student_ID already existed')
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')

        return cleaned_data

class LoginForm(forms.Form):

    username = forms.CharField(
        label='Username or Student_ID',
        min_length=2,
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )