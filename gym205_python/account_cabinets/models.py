from django.db import models
from django.contrib.auth.models import User

from requests import request



class Document(models.Model):
    docfile = models.FileField(upload_to='test')



# # работает
# def user_directory_path(instance, filename):
#     extension = filename.split('.')[-1]
#
#     # instance.user_id - это сама модель с которой работаем (Document) и .user_id это поле .user_id
#     print(instance.user_id)
#     return "students_files/{0}/profile_picture.{1}".format(instance.user_id, extension)
#
# class Document(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     docfile = models.FileField(upload_to=user_directory_path)
#     date = models.DateTimeField(auto_now_add=True, blank=True)