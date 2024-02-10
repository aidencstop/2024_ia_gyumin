from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('student-login/', views.student_login, name='student-login'),
    path('student-logout/', views.student_logout, name='student-logout'),
    path('student-main/', views.student_main, name='student-main'),
    path('student-initial/', views.student_initial, name='student-initial'),
    path('student-edit/', views.student_edit, name='student-edit'),
    path('student-recommend/', views.student_recommendation, name='student-recommend'),
    path('student-recommend-pdf/', views.student_recommendation_pdf, name='student-recommendation-pdf'),

    path('fetch-activities/', views.fetch_activities, name='fetch-activities'),

]