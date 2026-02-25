from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random

from jobs.models import Job
from applications.models import Application

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with dummy data"

    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.SUCCESS("Deleting old data..."))

        Application.objects.all().delete()
        Job.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create Recruiters
        recruiters = []
        for i in range(3):
            recruiter = User.objects.create_user(
                username=f"recruiter{i+1}",
                email=fake.email(),
                password="password123"
            )
            recruiters.append(recruiter)

        # Create Job Seekers
        seekers = []
        for i in range(10):
            seeker = User.objects.create_user(
                username=f"seeker{i+1}",
                email=fake.email(),
                password="password123"
            )
            seekers.append(seeker)

        job_titles = [
            "Python Django Developer",
            "React Frontend Engineer",
            "DevOps Engineer",
            "Cyber Security Analyst",
            "AI/ML Engineer",
            "Data Scientist",
            "Full Stack Developer",
            "Backend API Developer",
            "Cloud Engineer",
            "Software Engineer"
        ]

        locations = [
            "Bangalore",
            "Hyderabad",
            "Pune",
            "Mumbai",
            "Delhi",
            "Chennai",
            "Remote"
        ]

        companies = [
            "TechNova Solutions",
            "CodeCraft Systems",
            "SecureNet Pvt Ltd",
            "DataBridge AI",
            "CloudScale Technologies"
        ]

        # Create Jobs
        jobs = []
        for i in range(25):
            job = Job.objects.create(
                title=random.choice(job_titles),
                description=fake.text(max_nb_chars=300),
                location=random.choice(locations),
                salary=f"{random.randint(4,15)} LPA",
                company_name=random.choice(companies),
                posted_by=random.choice(recruiters)
            )
            jobs.append(job)

        # Create Applications
        for i in range(40):
            Application.objects.create(
                job=random.choice(jobs),
                applicant=random.choice(seekers),
                status=random.choice(["Pending", "Reviewed", "Accepted", "Rejected"])
            )

        self.stdout.write(self.style.SUCCESS("Dummy data created successfully!"))
        