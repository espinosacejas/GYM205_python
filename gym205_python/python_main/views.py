from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.mail import send_mail
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .email_code import email_check
from django.core.mail import send_mail

import random

import mysql.connector
from time import sleep
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth





con = mysql.connector.connect(user='alex',
                              password='nazca007',
                              host='127.0.0.1',
                              database='gym205_python_base')

mycursor = con.cursor()




def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))



def start_index(request):
    # Форма регистрации пользователя
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()

            # достаем из одобренной формы данные через cleaned_data
            email_search = user_form.cleaned_data['email']
            name_search = user_form.cleaned_data['first_name']

            #ищем юзера по таблице БД нам нужен его ID
            query = ("SELECT id FROM auth_user WHERE email=%s")
            mycursor.execute(query, (email_search,))
            result_list = mycursor.fetchall()
            result_id = ''
            for x in result_list:
                for item in x:
                    result_id = item


            check_code = generate_code()


            insert_data_code = """
                INSERT INTO python_main_user_verification_code (user_id_id, verification_code, status)
                VALUES ( %s, %s, %s ) """
            data_records = [f'{result_id}', f'{check_code}', 0]
            with con.cursor() as cursor:
                cursor.execute(insert_data_code, data_records)
                con.commit()

            sleep(1)
            # создаем рандомный пароль, его сохраним в базу и отправим на почту. потом человек открывает почту
            # и там будет не только пароль, но и ссылка, он переходит. вбивает свою почту и пароль и если все хорошо
            # (проверка по базе данных), то его аккаунт становится активным.
            mail = send_mail(f'{check_code}', f'Уважаемый {name_search} Вам нужно пройти по ссылке и ввести почту + код: {check_code}, для активации'
                                              f'аккаунта', 'erapyth@gmail.com',
                             [f'{email_search}'], fail_silently=False)




            return render(request, 'python_main/start_index.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'python_main/start_index.html', {'user_form': user_form})


# Блок страницы с регистрацией пользователя
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('start_index')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')
    else:
        return render(request, 'python_main/registration/login_index.html')





###########______Блок основной части сайта______###########

## Создаем декоратор @group_required, чтобы проверять входят ли пользователи в дозволенную группу ##
# дальше мы можем просто в скобках декоратора давать группы для проверки
def check_user_able_to_see_page(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            else:
                not_registr = 'Вы не можете посетить сайт, без регистрации!'
                return render(request, 'python_main/start_index.html', {'not_registr': not_registr})

        return wrapper

    return decorator

# ссылки обучения https://pythonist.ru/top-6-dekoratorov-v-django/
# https://pythonist.ru/top-6-dekoratorov-v-django/


@check_user_able_to_see_page('students')
def main_index(request):
    return render(request, 'python_main/main_index.html')