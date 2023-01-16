from django.contrib.auth.models import User
from django.db import models


class user_verification_code(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_code = models.TextField('сюда вставляется сгенерированный код')
    status = models.BooleanField('активирован?', default=False)


    def __str__(self):
        return self.verification_code

    class Meta:
        verbose_name = 'Подтверждение акканута'
        verbose_name_plural = 'Подтверждение акканута'
