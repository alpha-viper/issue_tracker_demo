from django.db import models
from users.models import User
# Create your models here.

class Project(models.Model):
    
    

    title=models.CharField(max_length=100,null=False)
    description = models.TextField(default="No description provided")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members=models.ManyToManyField(User,through='ProjectTag')
    owner=models.ForeignKey("users.User",related_name="owned_project",on_delete=models.CASCADE)
   

class ProjectTag(models.Model):
    
    
    ROLES = (
        (1, "Project Manager"),
        (2, "Project Member"),
    )
    project=models.ForeignKey("projects.Project",null=True,on_delete=models.CASCADE);
    user=models.ForeignKey("users.User",null=True,on_delete=models.CASCADE);
    role = models.IntegerField(choices=ROLES, default=2)
    