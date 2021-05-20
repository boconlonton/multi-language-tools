from django.db import models
from django.contrib.auth.models import User
from project.models import Project


class Screen(models.Model):
    """Screen model"""
    screen_code = models.CharField(max_length=255, unique=True)
    screen_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.TextField()
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_modified')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created')
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.screen_code
