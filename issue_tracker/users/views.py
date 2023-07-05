from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from users.models import User
from users.serializers import UserSerializer
from django.contrib import messages





class MembersViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer


