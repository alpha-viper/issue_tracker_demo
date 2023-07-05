from django.shortcuts import render,redirect
from rest_framework import viewsets
from projects.models import Project,ProjectTag
from projects.serializers import ProjectSerializer
from django.contrib import messages
from django.views import View
from django.views.generic.base import TemplateView
from users.models import User
from django.http import request
from django.contrib.auth.mixins import LoginRequiredMixin

# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import BasePermission, IsAuthenticated

class ProjectsViewSet(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/create_projects.html"
    login_url = "signin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.exclude(id=self.request.user.id)
        context["users"] = users
        return context

    def post(self, request):
        print(request.POST)
       
        data = {
            "title": request.POST.get('title'),
            "description": request.POST.get('description'),
            "members": [],
            "owner": request.user.id,
        }
        serializer = ProjectSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            project = serializer.save()
            members = request.POST.getlist("members")
            for member_id in members:
                user = User.objects.get(id=member_id)
                role = request.POST.get(f"member_role_{member_id}")
                ProjectTag.objects.create(user=user, project=project, role=role)

            messages.success(request, "Project has been successfully created")
            return render(request,'dashboard/user.html')
        else:
            context = self.get_context_data(serializer_errors=serializer.errors)
            return self.render_to_response(context)


class ProjectEditView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/edit_project.html"
    login_url = "signin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get("project_id")
        project = Project.objects.get(id=project_id)

        if self.request.user == project.owner:
            users = User.objects.exclude(id=self.request.user.id)
        else:
            users = None
        context["project"] = project
        context["users"] = users
        return context

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        members = request.POST.getlist("members[]")

        ProjectTag.objects.filter(project=project).delete()

        for member_id in members:
            user = User.objects.get(id=member_id)
            role = request.POST.get(f"member_role_{member_id}", 2)
            member = ProjectTag.objects.create(user=user, project=project, role=role)

        project_serializer = ProjectSerializer(
            project, data=request.POST, context={"request": request}
        )

        if project_serializer.is_valid():
            project_serializer.save()
            messages.success(request, "Project has been successfully updated")
            return redirect("authentication:dashboard")
        else:
            context = self.get_context_data()
            context["project_serializer_errors"] = project_serializer.errors




class home(TemplateView):

       queryset=User.objects.all()
       template_name = 'dashboard/create_projects.html'
       extra_context={'user_list': queryset}

