from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #-----------------------------------------Justine------------------------------------------------
    re_path(r'^accounts/login/$', views.login2, name='login2'),
    re_path(r'^accounts/signup/$', views.signup, name='signup'),
  


























    #----------------------------------------Ferryl------------------------------------------------
  re_path(r'^try$', views.trys, name='try'),
  re_path(r'^index$', views.index, name='index'),
  re_path(r'^register$', views.register, name='register'),
  re_path(r'^validatelogin$', views.validatelogin, name='validatelogin'),
  re_path(r'^studentdashboard$', views.studentdashboard, name='studentdashboard'),
  































    #------------------------------------------Erwin------------------------------------------------

    path('calendar/', views.schedule_view, name='CalendarSchedule'),  
    path('calendar/schedule/', views.AddSchedule, name='AddSchedule'),  
    path('calendar/schedule-list/', views.schedule_list, name='schedule_list'),  
    path('schedules/update/<int:schedule_id>/', views.update_schedule, name='update_schedule'),  
    path('schedules/delete/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),


    path('schedule_list/', views.schedule_list, name='schedule_list'),



























]

