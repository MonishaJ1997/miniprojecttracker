from rest_framework import serializers
from .models import MiniProject, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','is_trainer','is_trainee']

class MiniProjectSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='assigned_to')

    class Meta:
        model = MiniProject
        fields = ['id','title','description','due_date','priority','status','assigned_to','assigned_to_id']

