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
from datetime import date
from pathlib import Path

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
        try:
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

                #сохраняем нашего юзера в БД verification
                insert_data_code = """
                    INSERT INTO python_main_user_verification_code (user_id_id, verification_code, status, email)
                    VALUES ( %s, %s, %s, %s ) """
                data_records = [f'{result_id}', f'{check_code}', 0, f'{email_search}']
                with con.cursor() as cursor:
                    cursor.execute(insert_data_code, data_records)
                    con.commit()

                verification_name_field = 'код для Верификации'
                #ищем код учителя для регистрации, чтобы отправить сразу на почту
                query = ("SELECT teacher_code_line FROM python_main_teacher_code_model WHERE teacher_code_name=%s")
                mycursor.execute(query, (verification_name_field,))
                result_list = mycursor.fetchall()
                teacher_code_result = ''
                for x in result_list:
                    for item in x:
                        teacher_code_result = item

                # создаем рандомный пароль, его сохраним в базу и отправим на почту. потом человек открывает почту
                # и там будет не только пароль, но и ссылка, он переходит. вбивает свою почту и пароль и если все хорошо
                # (проверка по базе данных), то его аккаунт становится активным.
                mail = send_mail(f'{check_code}', f'Уважаемый ---- {name_search} ---- Вам нужно пройти '
                                                  f'по ссылке http://127.0.0.1:8000/verification_ind и ввести:\n\n'
                                                  f'свою почту: {email_search} \n\n'
                                                  f'код верификации: {check_code} \n\n'
                                                  f'код учителя: {teacher_code_result} \n\n', 'erapyth@gmail.com',
                                 [f'{email_search}'], fail_silently=False)


                messages.success(request, 'Аккаунт создан, проверьте почту для завершения регистрации')
                return render(request, 'python_main/start_index.html', {'new_user': new_user})

        except:
            messages.error(request, 'Вы ввели некорректные данные. Почта уже используется')
            return render(request, 'python_main/start_index.html')

    else:
        user_form = UserRegistrationForm()

    return render(request, 'python_main/start_index.html', {'user_form': user_form})



###########______Контакт с разработчиками с главной страницы______###########
def contact_start(request):
    if request.method == 'POST':
        contact_email = request.POST['contact_mail']
        contact_message = request.POST['contact_message']

        time_date = date.today()

        if '@' in contact_email:
            insert_data_code = """
                INSERT INTO python_main_contact_teacher_start_page (email_contact_start, text_contact_start, date)
                VALUES ( %s, %s, %s ) """
            data_records = [f'{contact_email}', f'{contact_message}', f'{time_date}']
            with con.cursor() as cursor:
                cursor.execute(insert_data_code, data_records)
                con.commit()
            messages.success(request, 'Обращение к администраторам сайта отправлено')
        else:
            messages.error(request, 'Ошибка, сообщение не отправлено, проверьте данные')
    return render(request, 'python_main/start_index.html')




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


# после создания аккаунта, надо пройти верификацию по ссылке
def verification_ind(request):
    if request.method == 'POST':
        try:
            email_done = request.POST['email']
            registr_code = request.POST['registr_code']
            teacher_code = request.POST['teacher_code']

            #у нас есть email юзера, теперь достаем его верификационный код
            query0 = ("SELECT verification_code FROM python_main_user_verification_code WHERE email=%s")
            mycursor.execute(query0, (email_done,))
            result_list = mycursor.fetchall()
            email_verif_code = ''
            for x in result_list:
                for item in x:
                    email_verif_code = item


            # проверяем если код из бд совпадает с кодом, который ввел пользователь, то идем дальше
            # ищем id user / group чтобы их дальше связать вместе
            if str(registr_code) == str(email_verif_code):

                query = ("SELECT id FROM auth_user WHERE email=%s")
                mycursor.execute(query, (email_done,))
                result_list = mycursor.fetchall()
                result_id_user = ''
                for x in result_list:
                    for item in x:
                        result_id_user = item

                name_group = 'students'

                #находим ID group по названию
                query = ("SELECT id FROM auth_group WHERE name=%s")
                mycursor.execute(query, (name_group,))
                result_list = mycursor.fetchall()
                result_id_group = ''
                for x in result_list:
                    for item in x:
                        result_id_group = item

                #сохраняем сводную таблицу user_groups
                insert_data_code = """
                    INSERT INTO auth_user_groups (user_id, group_id)
                    VALUES ( %s, %s ) """
                data_records = [f'{result_id_user}', f'{result_id_group}']
                with con.cursor() as cursor:
                    cursor.execute(insert_data_code, data_records)
                    con.commit()

                query = ("SELECT username FROM auth_user WHERE id=%s")
                mycursor.execute(query, (result_id_user,))
                result_list = mycursor.fetchall()
                result_username = ''
                for x in result_list:
                    for item in x:
                        result_username = item

                #создаем папку под студента
                Path(f"account_cabinet/files_students/{result_username}").mkdir(parents=True, exist_ok=True)
                # создаем папку под студента

                messages.success(request, 'Верификация успешно пройдена. Теперь Вы можете залогиниться и зайти на сайт')
                return render(request, 'python_main/start_index.html')

            messages.error(request, 'Данные не подтверждены')
            return render(request, 'python_main/registration/verification_index.html')
        except:
            messages.error(request, 'Данные не подтверждены')
            return render(request, 'python_main/registration/verification_index.html')
    else:
        return render(request, 'python_main/registration/verification_index.html')




###########______Блок основной части сайта______###########

## Создаем декоратор @group_required, чтобы проверять входят ли пользователи в дозволенную группу ##
# дальше мы можем просто в скобках декоратора давать группы для проверки
def check_user_able_to_see_page(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            else:
                not_registr = 'Вы не можете посетить сайт, без полной регистрации!'
                return render(request, 'python_main/start_index.html', {'not_registr': not_registr})

        return wrapper

    return decorator

# ссылки обучения https://pythonist.ru/top-6-dekoratorov-v-django/
# https://pythonist.ru/top-6-dekoratorov-v-django/


@check_user_able_to_see_page('students')
def main_index(request):
    today = date.today()
    date_now = today.strftime("%B %d, %Y")
    user_id = request.user.id

    query = ("SELECT email FROM auth_user WHERE id=%s")
    mycursor.execute(query, (user_id,))
    result_list = mycursor.fetchall()
    result_email = ''
    for x in result_list:
        for item in x:
            result_email = item

    if result_email == '':
        result_email = 'почта не указана'
    return render(request, 'python_main/main_index.html', {'date_now': date_now, 'result_email': result_email})