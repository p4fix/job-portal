from django.db import models
from django.contrib.auth.models import User


class Role(models.TextChoices):
    JOB_SEEKER = 'job_seeker', 'Job Seeker'
    RECRUITER = 'recruiter', 'Recruiter'


class Profile(models.Model):
    """Extends Django User with role, phone, and profile picture."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    @property
    def is_job_seeker(self):
        return self.role == Role.JOB_SEEKER

    @property
    def is_recruiter(self):
        return self.role == Role.RECRUITER
