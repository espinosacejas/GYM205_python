from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from .forms import *
from django.urls import reverse

from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.core.mail import send_mail
from datetime import date
from pathlib import Path
from django.core.files.storage import FileSystemStorage

import random
import os

import mysql.connector
from time import sleep
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth





con = mysql.connector.connect(user='alex',
                              password='nazca007',
                              host='127.0.0.1',
                              database='gym205_python_base')

mycursor = con.cursor()




def personal_account(request):
    today = date.today()
    date_now = today.strftime("%B %d, %Y")
    user_id = request.user.id

    # тут мы поулчаем кортеж с 2 данными требуемыми
    query = ("SELECT email, username FROM auth_user WHERE id=%s")
    mycursor.execute(query, (user_id,))
    result_list = mycursor.fetchall()
    result_email = ''
    result_login = ''
    for x in result_list:
        result_email = x[0]
        result_login = x[1]

    if result_email == '':
        result_email = 'почта не указана'

    # получаем список всех файлов в папке ученика
    try:
        dirname = f'account_cabinets/files_students/{result_login}/'
        all_files = os.listdir(dirname)
        error_files = ''
        if len(all_files) == 0:
            error_files = 'У Вас нет файлов.'
    except:
        all_files = ''
        error_files = 'Файлы не найдены, обратитесь к администратору'

    #загрузка файла на сервер
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Файл успешно загружен')
            return redirect('personal_account')
    else:
        form = DocumentForm


    return render(request, 'account_cabinet/account_cab.html',
                  {'date_now': date_now, 'result_email': result_email,
                   'result_login': result_login, 'all_files': all_files,
                   'error_files': error_files, 'form': form})





def upload(request):
    if request.method == 'POST':
        print('yes1')
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            print('yes2')
            form.save()
            return render(request, 'account_cabinet/account_cab.html')
    else:
        form = DocumentForm
    return render(request, 'account_cabinet/account_cab.html')
