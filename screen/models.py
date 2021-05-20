from django.db import models
from django.contrib.auth.models import User


class Screen(models.Model):
    """Screen model"""
    screen_code = models.CharField(max_length=255, unique=True)
    screen_name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.TextField()
    project = models.ForeignKey(to='Project', on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_modified')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created')
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
