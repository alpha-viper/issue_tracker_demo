from django.shortcuts import render,redirect
from stories.models import Story
from users.serializers import UserSerializer
from django.contrib import messages
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from projects.models import Project,ProjectTag
from stories.serializers import StorySerializer
from users.models import User
from django.conf import settings
from django.core.mail import send_mail


class CreateStoryView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/add_story.html"
    login_url = "signin"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        project_id=self.kwargs["project_id"]
        print(project_id)
        project=Project.objects.get(id=project_id)  

        if(self.request.user in project.members.all() 
        or self.request.user == project.owner):
            users=project.members.all()
        else:
            users=None
        
        context["project"]=project
        context["users"]=users
          
        return context
    
    
    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "assignee": request.POST.get("assignee"),
            "estimated_time": request.POST.get("estimate"),
            "project": project_id,
        }
        serializer = StorySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Story has been successfully created")
            assignee_id = request.POST.get("assignee")
            assignee = User.objects.get(id=assignee_id)

            subject = 'Assigned to a new story'
            message = f"You've been assigned to the story '{serializer.data['title']}' in {project.title}."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [assignee.email]
            send_mail( subject, message, email_from, recipient_list )
            return redirect("authentication:dashboard")
        else:
            context = self.get_context_data()
            context["serializer_errors"] = serializer.errors
            return self.render_to_response(context)

class ViewStory(LoginRequiredMixin, TemplateView):
     template_name = "dashboard/story_view.html"
     login_url = "signin"

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs["project_id"]
        project = Project.objects.get(id=project_id)
        scheduled_stories = Story.objects.filter(project=project, is_scheduled=1
        , is_deleted=False).order_by("-status", "created_at")
        unscheduled_stories = Story.objects.filter(project=project, is_scheduled=2
       , is_deleted=False ).order_by("-status", "created_at")
        context["project"] = project
        context["scheduled_stories"] = scheduled_stories
        context["unscheduled_stories"] = unscheduled_stories
        return context


class UpdateStory(LoginRequiredMixin, TemplateView):
        template_name = "dashboard/update_story.html"
        login_url = "signin"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            project_id = self.kwargs["project_id"]
            story_id = self.kwargs["story_id"]
            project = Project.objects.get(id=project_id)
            story = Story.objects.get(id=story_id, project_id=project_id)

            if (
                self.request.user in project.members.all()
                or self.request.user == project.owner
            ):
                users = project.members.all()
            else:
                users = None
            
            context["project"] = project
            context["story"] = story
            context["users"] = users
            context["status_choices"] = Story.STATUS_CHOICES
            context["schedule_choices"] = Story.SCHEDULE_CHOICES
            return context

        def post(self, request, project_id, story_id):
            story = Story.objects.get(id=story_id)

            if story.status == 4:
                messages.error(request, "Delivered stories cannot be updated.")
                return self.get(request, project_id=project_id, story_id=story_id)

            if story.status in [2, 3] and request.POST.get("is_scheduled") == "2":
                messages.error(request, "Started/Finished stories cannot be unscheduled.")
                return self.get(request, project_id=project_id, story_id=story_id)

            if request.POST.get("is_scheduled") == "2" and story.status != 1:
                messages.error(
                    request,
                    "To unschedule a story, its state should be set to Not Started first.",
                )
                return self.get(request, project_id=project_id, story_id=story_id)

            serializer = StorySerializer(story, data=request.POST, partial=True)
            if serializer.is_valid():
                serializer.save()
                messages.success(request, "Story has been updated successfully")
                return redirect("stories:stories_list", project_id=project_id)
            else:
                context = self.get_context_data()
                context["serializer_errors"] = serializer.errors
                return self.render_to_response(context)


class StoryDeleteView(LoginRequiredMixin, View):
    
    login_url="signin"
    def post(self, request, project_id, story_id):
        story = Story.objects.get(id=story_id)
        story.is_deleted = True
        story.save()

        messages.success(request, "Story has been soft deleted")
        return redirect("stories:stories_list", project_id=project_id)


       
