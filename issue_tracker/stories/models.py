from django.db import models
from users.models import User
# Create your models here.

class Story(models.Model):
        STATUS_CHOICES = (
        (1, "Not Started"),
        (2, "Started"),
        (3, "Finished"),
        (4, "Delivered"),
        )

        SCHEDULE_CHOICES = (
        (1, "Scheduled"),
        (2, "Not Scheduled"),
        )
        
        title=models.CharField(max_length=100,null=False)
        is_scheduled=models.IntegerField(choices=SCHEDULE_CHOICES,default=2)
        description=models.TextField()
        status=models.IntegerField(choices=STATUS_CHOICES,default=1)
        project=models.ForeignKey("projects.Project",null=False, on_delete=models.CASCADE)
        assignee=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
        estimated_time=models.IntegerField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        is_deleted= models.BooleanField(default=False)