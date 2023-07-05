
from django.contrib import admin
from django.urls import path,include
from issue_tracker.views import home
from authentication import views

urlpatterns = [
    path('',include(('authentication.urls','authentication'),namespace="authentication")),
    path('users',include('users.urls')),
    path('projects/',include(('projects.urls','projects'),namespace="projects")),
    path("stories/", include(("stories.urls", "stories"), namespace="stories")),
]
