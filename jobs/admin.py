from django.contrib import admin
from .models import Job, SavedJob


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'category', 'job_type', 'posted_by', 'is_active', 'created_at')
    list_filter = ('created_at', 'location', 'category', 'job_type', 'experience_level', 'is_active')
    search_fields = ('title', 'company_name', 'location')
    readonly_fields = ('created_at',)


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'job__title')
