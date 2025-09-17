from django import forms
from .models import MiniProject
from django.contrib.auth import get_user_model

User = get_user_model()



# mini/forms.py
from django import forms
from .models import MiniProject

class MiniProjectForm(forms.ModelForm):
    class Meta:
        model = MiniProject
        fields = ['title', 'description', 'status', 'assigned_to', 'due_date']  # include due_date
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})  # HTML5 date picker
        }
