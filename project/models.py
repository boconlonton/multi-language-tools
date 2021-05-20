from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """Project model"""
    project_name = models.CharField(max_length=255, unique=True)
    project_description = models.TextField()
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_modified')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created')
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
