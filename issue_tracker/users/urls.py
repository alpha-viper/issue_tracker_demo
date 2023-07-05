from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from users.views import MembersViewSet
from . import views

router=routers.DefaultRouter()
router.register(r'users',MembersViewSet)
urlpatterns = [

    path('',include(router.urls)),

]