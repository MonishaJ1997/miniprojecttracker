from django.contrib import admin
from .models import User, MiniProject

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")

@admin.register(MiniProject)
class MiniProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_to", "due_date", "status")
