from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/create/', views.job_create, name='job_create'),
    path('job/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('job/<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('job/<int:pk>/save/', views.save_job, name='save_job'),
    path('job/<int:pk>/unsave/', views.unsave_job, name='unsave_job'),
    path('saved-jobs/', views.saved_jobs_list, name='saved_jobs'),
    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('seeker/dashboard/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
]
