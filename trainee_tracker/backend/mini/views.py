from rest_framework import viewsets, permissions
from .models import MiniProject, User
from .serializers import MiniProjectSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class MiniProjectViewSet(viewsets.ModelViewSet):
    queryset = MiniProject.objects.all()
    serializer_class = MiniProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)

        role = "trainer" if user.is_staff else "trainee"
        return JsonResponse({"success": True, "token": token.key, "role": role})
    else:
        return JsonResponse({"success": False, "error": "Invalid credentials"}, status=400)
    


from django.shortcuts import render

def home(request):
    return render(request, "index.html")


from django.shortcuts import redirect

def login_redirect(request):
    user = request.user
    if user.is_authenticated:
        if user.role == 'trainer':
            return redirect('trainer_dashboard')  # front-end trainer page
        elif user.role == 'trainee':
            return redirect('trainee_dashboard')  # front-end trainee page
        elif user.is_superuser:
            return redirect('/admin/')             # admin panel
    else:
        return redirect('/admin/login/')           # show login page if not logged in


from django.shortcuts import render

def trainer_dashboard(request):
    return render(request, 'trainer_dashboard.html')

def trainee_dashboard(request):
    return render(request, 'trainee_dashboard.html')


from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MiniProject
from .forms import MiniProjectForm  # make sure this form exists

@login_required
def create_project(request):
    if request.method == 'POST':
        form = MiniProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('trainer_dashboard')
    else:
        form = MiniProjectForm()
    return render(request, 'project_form.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .models import MiniProject
from .forms import MiniProjectForm

def update_project(request, pk):
    project = get_object_or_404(MiniProject, pk=pk)
    if request.method == 'POST':
        form = MiniProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('trainer_dashboard')  # redirect to trainer dashboard after update
    else:
        form = MiniProjectForm(instance=project)
    return render(request, 'update_project.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .models import MiniProject

def delete_project(request, pk):
    project = get_object_or_404(MiniProject, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('trainer_dashboard')  # redirect after deletion
    return render(request, 'delete_project.html', {'project': project})


from django.shortcuts import render, redirect, get_object_or_404
from .models import MiniProject
from .forms import MiniProjectForm

# Update project
def update_project(request, pk):
    project = get_object_or_404(MiniProject, pk=pk)
    if request.method == 'POST':
        form = MiniProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('trainer_dashboard')
    else:
        form = MiniProjectForm(instance=project)
    return render(request, 'update_project.html', {'form': form})

# Delete project
def delete_project(request, pk):
    project = get_object_or_404(MiniProject, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('trainer_dashboard')
    return render(request, 'delete_project.html', {'project': project})


def create_project(request):
    if request.method == "POST":
        form = MiniProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("trainer_dashboard")
    else:
        form = MiniProjectForm()  # blank form for GET

    return render(request, "project_form.html", {"form": form})


def trainer_dashboard(request):
    projects = MiniProject.objects.all()
    form = MiniProjectForm()  # always pass a blank form
    return render(request, "trainer_dashboard.html", {"projects": projects, "form": form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import MiniProject
from .forms import MiniProjectForm

def trainer_dashboard(request):
    # Handle project creation inline
    if request.method == "POST" and "create_project" in request.POST:
        form = MiniProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("trainer_dashboard")
    else:
        form = MiniProjectForm()

    projects = MiniProject.objects.all()
    return render(request, "trainer_dashboard.html", {"projects": projects, "form": form})


def update_project(request, pk):
    project = get_object_or_404(MiniProject, pk=pk)
    if request.method == "POST":
        form = MiniProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("trainer_dashboard")
    else:
        form = MiniProjectForm(instance=project)
    return render(request, "project_form.html", {"form": form})


def delete_project(request, pk):
    project = get_object_or_404(MiniProject, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect("trainer_dashboard")
    return render(request, "confirm_delete.html", {"project": project})

