from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('counselor-login/', views.counselor_login, name='counselor-login'),
    path('counselor-logout/', views.counselor_logout, name='counselor-logout'),
    path('counselor-main/', views.counselor_main, name='counselor-main'),
    path('counselor-checkstudents/<int:year>/', views.counselor_checkstudents, name='counselor-checkstudents'),
    path('counselor-editstudents/<int:id>/', views.counselor_editstudents, name='counselor-editstudents'),
    path('counselor-checkdetails/<int:id>/', views.counselor_checkdetails, name='counselor-checkdetails'),
    path('counselor-studentdashboard/', views.counselor_studentdashboard, name='counselor-studentdashboard'),
    path('counselor-studdashboarddetail/<int:id>/', views.counselor_studdashboarddetail, name='counselor-studdashboarddetail'),
]