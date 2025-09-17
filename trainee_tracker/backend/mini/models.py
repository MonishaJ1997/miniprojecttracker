# mini/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("trainer", "Trainer"),
        ("trainee", "Trainee"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="trainee")

    def __str__(self):
        return self.username


class MiniProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")])
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("in_progress", "In Progress"), ("completed", "Completed")], default="pending")
    
    # ✅ link to custom user
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.title
