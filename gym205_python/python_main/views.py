from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.mail import send_mail
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm

from .email_code import email_check
from django.core.mail import send_mail

import random

import mysql.connector
from time import sleep


con = mysql.connector.connect(user='alex',
                              password='nazca007',
                              host='127.0.0.1',
                              database='gym205_python_base')

mycursor = con.cursor()




def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))



def main_index(request):
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
                    print(item)
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




            return render(request, 'python_main/main_index.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'python_main/main_index.html', {'user_form': user_form})

