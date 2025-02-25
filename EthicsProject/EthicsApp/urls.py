from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.homeLogin, name='index'),
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
    path('update-thesis-info/', views.update_thesis_info, name='update_thesis_info'),
    path('completeProfile/', views.completeProfile, name='completeProfile'),
    path('addMemberStudent/', views.addMemberStudent, name='addMemberStudent'),
    re_path(r'^get_admin_schedule/$', views.get_admin_schedule, name='get_admin_schedule'),
    path('get_reviewers/<int:college_id>/', views.get_reviewers_by_college, name='get_reviewers_by_college'),
    path('save_claimStabs/', views.save_claimStabs, name='save_claimStabs'),
    path('assign_reviewer/', views.assign_reviewer, name='assign_reviewer'),



















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
  re_path(r'^api/schedulesReviewer/$', views.ReviewerScheduleDataView.as_view(), name='get_ReviewerSchedule_data'),



  re_path(r'^adminAddCategory/$', views.adminAddCategory, name='adminAddCategory'),
  re_path(r'^adminStudtype/$', views.adminStudtype, name='adminStudtype'),
  re_path(r'^adminBasicreq/$', views.adminBasicreq, name='adminBasicreq'),
  re_path(r'^adminSDreq/$', views.adminSDreq, name='adminSDreq'),
  re_path(r'^update_category/(?P<category_id>\d+)/$', views.update_category, name='update_category'),
  path('admin/get-appointment/<int:appointment_id>/', views.get_edit_appointment, name='get_edit_appointment'),

  path('admin/get_view_appointment/<int:appointment_id>/', views.get_view_appointment, name='get_view_appointment'),
  
 path('accounts_logout/', views.accounts_logout, name='accounts_logout'),
 path('reviewer_logout/', views.reviewer_logout, name='reviewer_logout'),
  path('admin_logout/', views.admin_logout, name='admin_logout'),





















    #------------------------------------------Erwin------------------------------------------------





    path('api/schedules/', views.schedule_list, name='schedule_list'),
    path('schedule/save/', views.save_schedule, name='save_schedule'),
    #path('api/appointments/', views.get_appointments, name='get_appointments'),
    #path('api/get_appointments/', views.get_appointments, name='get_appointments'),
    #path('students_appointments/', views.student_appointment, name='students_appointments'),

    re_path(r'^adminEthicalRiskQuestions/$', views.adminEthicalRiskQuestions, name='adminEthicalRiskQuestions'),
    re_path(r'^adminAddEthicalRiskQuestions/$', views.adminAddEthicalRiskQuestions, name='adminAddEthicalRiskQuestions'),
    re_path(r'^adminEditEthicalRiskQuestions/$', views.adminEditEthicalRiskQuestions, name='adminEditEthicalRiskQuestions'),

    re_path(r'^adminDeleteEthicalRiskQuestions/(?P<question_id>\d+)/$', views.adminDeleteEthicalRiskQuestions, name='adminDeleteEthicalRiskQuestions'),
    # path('api/schedulesReviewer/', views.AdminReviewerScheduleDataView.as_view(), name='admin_reviewer_schedule_data'),
    path('remove_reviewer/<int:reviewer_id>/', views.remove_reviewer, name='remove_reviewer'),
    path('resend_invite/<int:reviewer_id>/', views.resend_invite, name='resend_invite'),


    re_path(r'^adminEditCollege/(?P<college_id>\d+)/$', views.adminEditCollege, name='adminEditCollege'),


    path('adminDeleteCollege/<int:college_id>/', views.adminDeleteCollege, name='adminDeleteCollege'),































]
