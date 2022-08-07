from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import *
urlpatterns = [
   path('signup/freelancer/',FreelancerSignupView.as_view()),
   path('signup/client/',ClientSignupView.as_view()),
   path('login/',CustomAuthToken.as_view(),name='auth-token'),
   path('logout/',LogoutView.as_view(),name='logout'),
   path('freelancer/dashboard/',FreelancerOnlyView.as_view(),name='freelancerview'),
   path('client/dashboard/',ClientOnlyView.as_view(),name='client'),
   
]