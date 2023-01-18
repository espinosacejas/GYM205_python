from django.contrib import admin
from python_main.models import user_verification_code, teacher_code_model


@admin.register(user_verification_code)
class user_verification_code_mainAdmin(admin.ModelAdmin):
    list_display = ['email', 'verification_code']

@admin.register(teacher_code_model)
class teacher_code_model_mainAdmin(admin.ModelAdmin):
    list_display = ['teacher_code_name', 'teacher_code_line']