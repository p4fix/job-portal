from rest_framework import serializers
from django.contrib.auth.models import User

from jobs.models import Job
from accounts.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'role', 'role_display', 'phone', 'profile_picture')


class JobListSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    job_type_display = serializers.CharField(source='get_job_type_display', read_only=True)
    experience_level_display = serializers.CharField(source='get_experience_level_display', read_only=True)
    application_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'company_name', 'location', 'salary',
            'category', 'category_display', 'job_type', 'job_type_display',
            'experience_level', 'experience_level_display',
            'created_at', 'is_active', 'application_count',
        )

    def get_application_count(self, obj):
        return obj.get_application_count()


class JobDetailSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    job_type_display = serializers.CharField(source='get_job_type_display', read_only=True)
    experience_level_display = serializers.CharField(source='get_experience_level_display', read_only=True)
    application_count = serializers.SerializerMethodField()
    posted_by_username = serializers.CharField(source='posted_by.username', read_only=True)

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'company_name', 'location', 'salary', 'description',
            'requirements', 'category', 'category_display', 'job_type', 'job_type_display',
            'experience_level', 'experience_level_display',
            'posted_by_username', 'created_at', 'is_active', 'application_count',
        )

    def get_application_count(self, obj):
        return obj.get_application_count()
