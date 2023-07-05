from django.contrib import admin
from django.urls import path,include
from .views import CreateStoryView
from authentication import views
from rest_framework import routers
from stories.views import CreateStoryView,ViewStory,UpdateStory,StoryDeleteView



urlpatterns = [
    path( "create/<int:project_id>/", CreateStoryView.as_view(),name="create_story",),
    path("show/<int:project_id>/", ViewStory.as_view(), name="stories_list"),
    path("update/<int:project_id>/<int:story_id>/",UpdateStory.as_view(),
    name="update_story",
    ),
     path("delete/<int:project_id>/<int:story_id>/",StoryDeleteView.as_view(),
        name="delete_story",
    )
]
