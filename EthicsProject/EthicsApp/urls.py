from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index1/', views.index1, name='index1'),
    path('add_event/', views.add_event, name='add_event'),
    path('calendar/', views.calendar_view, name='calendar'),




    #-----------------------------------------Justine------------------------------------------------




























    #----------------------------------------Feryl------------------------------------------------
































    #------------------------------------------Erwin------------------------------------------------




























]

