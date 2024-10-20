from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #-----------------------------------------Justine------------------------------------------------
    re_path(r'^accounts/login/$', views.login2, name='login2'),
    re_path(r'^accounts/signup/$', views.signup, name='signup'),
    re_path(r'^adminDashboard/$', views.adminDashboard, name='adminDashboard'), 
    re_path(r'^adminAccounts/$', views.adminAccounts, name='adminAccounts'),
    re_path(r'^adminAppointments/$', views.adminAppointments, name='adminAppointments'),
    re_path(r'^adminManuscripts/$', views.adminManuscripts, name='adminManuscripts'),
    re_path(r'^adminSchedule/$', views.adminSchedule, name='adminSchedule'),
    re_path(r'^adminSettings/$', views.adminSettings, name='adminSettings'),
    re_path(r'^adminHelpSupport/$', views.adminHelpSupport, name='adminHelpSupport'),
    re_path(r'^ScheduleView/$', views.ScheduleView.as_view(), name='ScheduleView'),
    re_path(r'^api/schedules/$', views.ScheduleDataView.as_view(), name='get_schedule_data'),
    path('schedules/edit/<int:scheduleId>/', views.edit_schedule, name='edit_schedule'),
    path('send_invitation_email/', views.send_invitation_email, name='send_invitation_email'),
    path('set-password/<uidb64>/<token>/', views.set_password, name='set_password'),

















    #----------------------------------------Ferryl------------------------------------------------
  re_path(r'^trys$', views.trys, name='trys'),
  re_path(r'^index$', views.index, name='index'),
  re_path(r'^register$', views.register, name='register'),
  re_path(r'^validatelogin$', views.validatelogin, name='validatelogin'),
  re_path(r'^studentdashboard$', views.studentdashboard, name='studentdashboard'),
  re_path(r'^studentAppointment$', views.studentAppointment, name='studentAppointment'),
  































    #------------------------------------------Erwin------------------------------------------------

    path('Reviewer/calendar/', views.schedule_view, name='schedule_view'),  
    path('Reviewer/calendar/schedule/', views.AddSchedule, name='AddSchedule'), 
    path('Reviewer/calendar/schedule2/', views.AddSchedule2, name='AddSchedule2'), 
    path('Reviewer/calendar/schedule-list/', views.schedule_list, name='schedule_list'),  
    path('schedules/update/<int:schedule_id>/', views.update_schedule, name='update_schedule'),  
    path('schedules/delete/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('Reviewer/dashboard/', views.dashboard, name='schedule_dashboard'),


    path('schedule_list/', views.schedule_list, name='schedule_list'),



























]

