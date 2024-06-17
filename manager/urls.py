from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('manager-login/', views.manager_login, name='manager-login'),
    path('manager-logout/', views.manager_logout, name='manager-logout'),
    path('manager-main/', views.manager_main, name='manager-main'),

    path('manager-addcounselor/', views.manager_addcounselor, name='manager-addcounselor'),
    path('manager-counselorlist/', views.manager_counselorlist, name='manager-counselorlist'),
    path('manager-studentlist/', views.manager_studentlist, name='manager-studentlist'),
    path('manager-addnewuser/', views.manager_addnewuser, name='manager-addnewuser'),
    path('manager-manageusers/', views.manager_manageusers, name='manager-manageusers'),
    path('manager-manageuni/', views.manager_manageuni, name='manager-manageuni'),
    path('manager-managemajors/', views.manager_managemajors, name='manager-managemajors'),
    path('manager-managecatact/', views.manager_managecatact, name='manager-managecatact'),
    
    path('manager-addcat/', views.manager_addcat, name='manager-addcat'),
    path('manager-addact/', views.manager_addact, name='manager-addact'),
    path('manager-addmajors/', views.manager_addmajors, name='manager-addmajors'),
    path('manager-adduni/', views.manager_adduni, name='manager-adduni'),
    
    path('manager-deleteuni/', views.Delete_uni.as_view(), name='manager-deleteuni'),
    path('manager-deletemajor/', views.Delete_major.as_view(), name='manager-deletemajor'),
    path('manager-deletecatact/', views.Delete_catact.as_view(), name='manager-deletecatact'),
    # path('manager-deleteuser/', views.Delete_user.as_view(), name='manager-deleteuser'),
    path('manager-deletecounselor/<int:id>/', views.manager_deletecounselor, name='manager-deletecounselor'),
    path('manager-deletestudent/<int:id>/', views.manager_deletestudent, name='manager-deletestudent'),
    path('manager-deletecategory/<int:id>/', views.manager_deletecategory, name='manager-deletecategory'),
    path('manager-editcategory/<int:id>/', views.manager_editcategory, name='manager-editcategory'),
    path('manager-addcategory/', views.manager_addcategory, name='manager-addcategory'),
]