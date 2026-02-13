from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'posted_by', 'created_at')
    list_filter = ('created_at', 'location')
    search_fields = ('title', 'company_name', 'location')
    readonly_fields = ('created_at',)
