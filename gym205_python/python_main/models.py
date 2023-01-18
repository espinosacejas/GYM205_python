from django.contrib.auth.models import User
from django.db import models


class user_verification_code(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField('сюда вставляется почта', max_length=300, null=True, unique=True)
    verification_code = models.IntegerField('сюда вставляется сгенерированный код')
    status = models.BooleanField('активирован?', default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Подтверждение акканута'
        verbose_name_plural = 'Подтверждение акканута'


class teacher_code_model(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    teacher_code_name = models.CharField('сюда название кода - для чего', max_length=200)
    teacher_code_line = models.IntegerField('сюда вставляется код')
    status = models.BooleanField('активирован?', default=False)


    def __str__(self):
        return self.teacher_code_name

    class Meta:
        verbose_name = 'Учительский код для регистрации'
        verbose_name_plural = 'Учительский код для регистрации'