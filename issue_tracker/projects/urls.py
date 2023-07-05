from django.contrib import admin
from django.urls import path,include
from users.models import User
from projects.views import home,ProjectsViewSet,ProjectEditView



urlpatterns = [
    path('',home.as_view()),
    path('api/project',ProjectsViewSet.as_view()),
    path("project_edit/<int:project_id>/",ProjectEditView.as_view(),
        name="project_edit",)
]
