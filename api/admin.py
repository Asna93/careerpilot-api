from django.contrib import admin

from .models import AIAnalysis, InterviewPrep, JobApplication, Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'file_type', 'is_default', 'uploaded_at']
    list_filter = ['file_type', 'is_default', 'uploaded_at']
    search_fields = ['name', 'user__username']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company_name', 'user', 'status', 'date_applied']
    list_filter = ['status', 'job_type', 'date_applied']
    search_fields = ['job_title', 'company_name', 'user__username']


@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    list_display = ['application', 'match_score', 'match_level', 'created_at']
    list_filter = ['match_level', 'created_at']
    search_fields = ['application__job_title']


@admin.register(InterviewPrep)
class InterviewPrepAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company', 'application', 'created_at']
    list_filter = ['created_at']
    search_fields = ['job_title', 'company']
