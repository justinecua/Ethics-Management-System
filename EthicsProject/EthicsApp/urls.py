from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #-----------------------------------------Justine------------------------------------------------
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^signup/$', views.signup, name='signup'),


























    #----------------------------------------Feryl------------------------------------------------
































    #------------------------------------------Erwin------------------------------------------------




























]

