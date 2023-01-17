from django.urls import path
from django.urls import include, re_path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from . import views



urlpatterns = [

########################### RUS PART ###########################
    path('', views.start_index, name='start_index'),
    path('login_user', views.login_user, name='login_user'),
    path('gym205', views.main_index, name='main_index'),
    # ниже ссылка с готовой View для создания ссылки на выход из аккаунта
    re_path(r'^logout$', LogoutView.as_view(), name='logout'),

]