from django.db import models
from django.contrib.auth.models import User

from jobs.models import Job


class ApplicationStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    ACCEPTED = 'Accepted', 'Accepted'
    REJECTED = 'Rejected', 'Rejected'


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-applied_at']
        unique_together = [['job', 'applicant']]

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title} ({self.status})"
