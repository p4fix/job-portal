from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    # JWT token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # API views (JWT optional for list/detail; required for profile)
    path('jobs/', views.JobListView.as_view(), name='api_job_list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='api_job_detail'),
    path('me/', views.CurrentUserProfileView.as_view(), name='api_current_user'),
]
