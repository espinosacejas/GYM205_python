from django.urls import path
from django.urls import include, re_path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from . import views



urlpatterns = [
    # личный кабинет
    path('personal_account', views.personal_account, name='personal_account'),
    # Загрузка файлов

    path('upload', views.upload, name='upload'),

]