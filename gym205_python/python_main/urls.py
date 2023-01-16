from django.urls import path
from . import views



urlpatterns = [

########################### RUS PART ###########################
    path('', views.main_index, name='main_index'),

]