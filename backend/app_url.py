# from django.contrib import admin
from django.urls import path
from . import views, admin_view

urlpatterns = [

    # Pages
    path('', views.home,name="home"),

    path('searchPage/<int:category>/<slug:query>/', views.searchPage,name="searchPage"),
    path('searchPage', views.searchPage,name="search_page"),

    path('file_like', views.file_like,name="file_like"),
    path('file_unlike', views.file_unlike,name="file_unlike"),
    path('add_bookmark', views.add_bookmark,name="add_bookmark"),
    path('remove_bookmark', views.remove_bookmark,name="remove_bookmark"),
    path('report_submit', views.report_submit,name="report_submit"),

    path('upload_page', views.upload_page,name="upload_page"),

    path('loginpage', views.loginpage , name="loginpage"),
    path('logout', views.logout , name="logout"),

    path('signuppage', views.signuppage , name="signuppage"),
    path('otp_page', views.otp_page , name="otp_page"),

    path('profile', views.profile , name="profile"),
    
    path('contact', views.contact , name="contact"),
    path('about', views.about,name="about"),

    path('adminfeed', admin_view.adminfeed , name="adminfeed"),
    path('changeRole', admin_view.changeRole , name="changeRole"),
    path('adminUserReports', admin_view.admin_user_reports , name="admin_user_reports"),
]
