from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(SugarTest)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(EducationalContent)
