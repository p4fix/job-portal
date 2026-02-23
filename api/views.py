from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.models import Job
from accounts.models import Profile
from .serializers import JobListSerializer, JobDetailSerializer, ProfileSerializer


class JobListView(generics.ListAPIView):
    """List all active jobs. Public (no JWT required)."""
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobListSerializer
    permission_classes = [AllowAny]


class JobDetailView(generics.RetrieveAPIView):
    """Retrieve a single job. Public (no JWT required)."""
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobDetailSerializer
    permission_classes = [AllowAny]


class CurrentUserProfileView(APIView):
    """Get current user profile. Requires JWT."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=404)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
