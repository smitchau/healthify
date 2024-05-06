"""
URL configuration for Healthify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('otp/', views.otp, name='otp'),
    path('password/', views.password, name='password'),
    path('index/', views.home, name='home'),
    path('book_appointment/<int:pk>/', views.book_appointment, name='book_appointment'),
    # path('add-patients/', views.add_patients, name='add-patients'),
    path('all-patients/', views.all_patients, name='all-patients'),
    path('invoice/', views.invoice, name='invoice'),
    path('patients-profile/<int:pk>', views.patients_profile, name='patients-profile'),
    path('approved/<int:pk>', views.approved, name='approved'),
    path('rejected/<int:pk>', views.rejected, name='rejected'),
    path('add-doctor/', views.add_doctor, name='add-doctor'),
    path('doctors/', views.doctors, name='doctors'),
    # path('events/', views.events, name='events'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/', views.myprofile, name='myprofile'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change_pass/', views.change_pass, name='change_pass'),
    path('Change_Picture/', views.Change_Picture, name='Change_Picture'),
]
