from django.urls import path
from . import views

urlpatterns = [
    path('home', views.webHomePage, name='home'),
    path('login', views.loginPage, name='login'),
    path('signup', views.signupPage, name='signup'),
    path('dashboard', views.dashBoardPage, name='dashboard'),
    path('otp', views.OTPPage, name='otpPage'), 
    path('forgot', views.forgotPage, name='forgotPage'),
    path('success', views.successPage, name='successPage'),
    path('failed', views.failedPage, name='failedPage'),
    path('locked', views.lockedPage, name='lockedPage'),
    path('appkey', views.appKeyPage, name='appkeyPage'),
    path('tc', views.termsAndConditionsPage, name='tcPage'),
    path('OTPDemo/', views.OTPGenerator, name='otpDemo'),
    path('OTPValidate/', views.OTPValidate, name='otpValidate'),
]