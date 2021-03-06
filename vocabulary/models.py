from django.db import models
from django.contrib.auth.models import User
from screen.models import Screen


class Vocabulary(models.Model):
    """Vocabulary model"""
    vocab_key = models.CharField(max_length=255, unique=True)
    english_definition = models.TextField(blank=True, null=True, default="")
    vn_definition = models.TextField(blank=True, null=True, default="")
    korean_definition = models.TextField(blank=True, null=True, default="")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_modified')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created')
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    screen = models.ManyToManyField(Screen)

    def __str__(self):
        return self.vocab_key
