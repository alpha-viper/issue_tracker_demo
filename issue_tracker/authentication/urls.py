from django.contrib import admin
from django.urls import path,include
from issue_tracker.views import home
from . import views
urlpatterns = [
    
    path('',views.home.as_view()),
    path('signin',views.signin.as_view(),name="signin"),
    path('signup',views.SignupView.as_view(),name="signup"),
    path('signout',views.signin.as_view(),name="signout"),
    path("dashboard",views.DashBoardView.as_view(),name="dashboard"),
    path("dashboard/<str:filter_param>/",views.DashBoardView.as_view(),name="filter"),
    path("profile",views.ProfileView.as_view(),name="view_profile"),
    path("edit",views.EditProfileView.as_view(),name="edit_profile")
]