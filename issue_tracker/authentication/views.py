from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from rest_framework import viewsets
from users.models import User
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from projects.models import Project
from users.serializers import UserSerializer
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
# Create your views here.

class home(View):
    def get(self,request):
        return render(request,"authentication/signin.html")


class SignupView(TemplateView):
    template_name = "authentication/signup.html"

    def post(self, request):
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, "Your account has been successfully created")
            subject = "Welcome to the Issue Tracker System"
            message = f"Hi {user.first_name}, thank you for registering in Issue Tracker System"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect("authentication:signin")
        else:
            context = self.get_context_data(serializer_errors=serializer.errors)
            return self.render_to_response(context, status=status.HTTP_400_BAD_REQUEST)
class signin(View):
    def post(self,request):
        
        email=request.POST.get('email')
        password=request.POST.get('password')

        user=authenticate(username=email,password=password)

        if user is not None:
            print(user)
            login(request,user)
            fname=user.first_name
            
            return redirect('authentication:dashboard')
        
        else:
            messages.error("Bad credentials")
            return redirect('authentication:signin')
    def get(self,request):
        return render(request,"authentication/signin.html")

class signout(View):
    def get(self,request):
        logout(request)
        messages.success("Logged out successfully")
        return redirect('home')

class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/user.html"
    login_url = "signin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        filter_param = self.kwargs.get("filter_param")

        if filter_param == "Owner":
            projects = Project.objects.filter(owner=user)
        elif filter_param == "Member":
            projects = Project.objects.filter(members=user)
        else:
            projects = Project.objects.filter(Q(members=user)|Q(owner=user))

        context["projects"] = projects
        context["fname"] = user.first_name
        return context



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/show_profile.html"
    login_url = "authentication:signin"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"]=user
        return context

class EditProfileView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/edit_profile.html"
    login_url = "authentication:signin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"]=user
        return context

    def post(self,request):
        print(request.user.email)
        user = User.objects.get(email=request.user.email)
        serializer = UserSerializer(user, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return redirect("authentication:view_profile")
        else:
            context = self.get_context_data(serializer_errors=serializer.errors)
            return self.render_to_response(context, status=status.HTTP_400_BAD_REQUEST)