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
    re_path(r'^adminColleges/$', views.adminColleges, name='adminColleges'),
    re_path(r'^adminAddColleges/$', views.adminAddColleges, name='adminAddColleges'),















    #----------------------------------------Ferryl------------------------------------------------
  re_path(r'^trys$', views.trys, name='trys'),
  re_path(r'^index$', views.index, name='index'),
  re_path(r'^register$', views.register, name='register'),
  re_path(r'^validatelogin$', views.validatelogin, name='validatelogin'),
  re_path(r'^studentdashboard/$', views.studentdashboard, name='studentdashboard'),
  re_path(r'^studentAppointment/$', views.studentAppointment, name='studentAppointment'),
  re_path(r'^studentManuscript/$', views.studentManuscript, name='studentManuscript'),
   re_path(r'^studentSettings/$', views.studentSettings, name='studentSettings'),


  re_path(r'^reviewerdashboard/$', views.reviewerdashboard, name='reviewerdashboard'),
  re_path(r'^reviewerManuscript/$', views.reviewerManuscript, name='reviewerManuscript'),
  re_path(r'^reviewerSchedule/$', views.reviewerSchedule, name='reviewerSchedule'),
  re_path(r'^reviewerSettings/$', views.reviewerSettings, name='reviewerSettings'),
  re_path(r'^ReviewerScheduleView/$', views.ReviewerScheduleView.as_view(), name='ReviewerScheduleView'),
  re_path(r'^api/schedules/$', views.ReviewerScheduleDataView.as_view(), name='get_ReviewerSchedule_data'),



  re_path(r'^adminAddCategory/$', views.adminAddCategory, name='adminAddCategory'),























    #------------------------------------------Erwin------------------------------------------------

    



    path('schedule_list/', views.schedule_list, name='schedule_list'),


    path('api/schedules/', views.schedule_list, name='schedule_list'),
    path('schedule/save/', views.save_schedule, name='save_schedule'),
    path('api/appointments/', views.get_appointments, name='get_appointments'),
    path('api/student_appointments/', views.get_appointments, name='get_appointments'),




























]

