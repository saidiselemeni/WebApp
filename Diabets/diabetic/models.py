from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Admin', 'Admin'),
    ]
    username = models.CharField(max_length=20, unique=True, blank=True, null=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(_('email address'), unique=True) 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    USERNAME_FIELD = 'email'  # use email to login
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Doctor(models.Model):
    doctor_name = models.CharField(max_length=100)
    address = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField()

    def __str__(self):
        return f"{self.doctor_name}"


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    patient_name = models.CharField(max_length=100)
    address = models.CharField(max_length=25)
    age = models.PositiveIntegerField()
    phone_no = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    password = models.CharField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.patient_name}"


class SugarTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='sugar_tests', null=True, blank=True)

    test_type = models.CharField(max_length=50)
    test_date = models.DateTimeField(auto_now_add=True)
    level = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.test_type}"


class Comment(models.Model):
    sugartest = models.ForeignKey(SugarTest, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.sugartest} by {self.id}'
from django.db import models


class EducationalContent(models.Model):
    FILE_TYPE_CHOICES = (
        ('document', 'Document'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='educational_files/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
