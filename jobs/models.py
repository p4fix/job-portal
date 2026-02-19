from django.db import models
from django.contrib.auth.models import User


class JobCategory(models.TextChoices):
    IT = 'IT', 'Information Technology'
    FINANCE = 'Finance', 'Finance'
    HEALTHCARE = 'Healthcare', 'Healthcare'
    EDUCATION = 'Education', 'Education'
    MARKETING = 'Marketing', 'Marketing'
    SALES = 'Sales', 'Sales'
    ENGINEERING = 'Engineering', 'Engineering'
    DESIGN = 'Design', 'Design'
    OTHER = 'Other', 'Other'


class JobType(models.TextChoices):
    FULL_TIME = 'Full-time', 'Full-time'
    PART_TIME = 'Part-time', 'Part-time'
    CONTRACT = 'Contract', 'Contract'
    INTERNSHIP = 'Internship', 'Internship'
    FREELANCE = 'Freelance', 'Freelance'


class ExperienceLevel(models.TextChoices):
    ENTRY = 'Entry', 'Entry Level'
    MID = 'Mid', 'Mid Level'
    SENIOR = 'Senior', 'Senior Level'
    EXECUTIVE = 'Executive', 'Executive'


class Job(models.Model):
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=JobCategory.choices, default=JobCategory.OTHER)
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.ENTRY)
    requirements = models.TextField(blank=True, help_text="Job requirements and qualifications")
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company_name}"

    def get_application_count(self):
        return self.application_set.count()

    def get_pending_applications_count(self):
        return self.application_set.filter(status='Pending').count()


class SavedJob(models.Model):
    """Allow job seekers to save/bookmark jobs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'job']]
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
