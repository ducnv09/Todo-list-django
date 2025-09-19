from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer cho User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer cho Task model"""
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'note', 'is_done', 'due_at', 'created_at', 'updated_at', 'owner']
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']
    
    def create(self, validated_data):
        """Tạo task mới với owner là user hiện tại"""
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer cho việc tạo và cập nhật Task (không bao gồm owner info)"""
    
    class Meta:
        model = Task
        fields = ['title', 'note', 'is_done', 'due_at']
    
    def create(self, validated_data):
        """Tạo task mới với owner là user hiện tại"""
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer cho đăng ký user mới"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Mật khẩu không khớp")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user
