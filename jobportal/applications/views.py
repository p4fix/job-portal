from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from jobs.models import Job
from accounts.models import Profile
from .models import Application
from .forms import ApplicationForm, ApplicationStatusForm


@login_required
def apply(request, job_pk):
    job = get_object_or_404(Job, pk=job_pk)
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('accounts:profile_update')
    if not profile.is_job_seeker:
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('jobs:job_detail', pk=job_pk)
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', pk=job_pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            messages.success(request, 'Application submitted successfully.')
            return redirect('jobs:job_detail', pk=job_pk)
        else:
            messages.error(request, 'Please correct the errors below. Only PDF resumes are accepted.')
    else:
        form = ApplicationForm()
    return render(request, 'applications/apply.html', {'form': form, 'job': job})


@login_required
def my_applications(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('accounts:profile_update')
    if not profile.is_job_seeker:
        messages.error(request, 'Access denied.')
        return redirect('jobs:job_list')
    applications = Application.objects.filter(applicant=request.user).select_related('job')
    return render(request, 'applications/my_applications.html', {'applications': applications})


@login_required
def job_applicants(request, job_pk):
    job = get_object_or_404(Job, pk=job_pk)
    if job.posted_by != request.user:
        messages.error(request, 'You can only view applicants for your own jobs.')
        return redirect('jobs:job_list')
    applications = Application.objects.filter(job=job).select_related('applicant')
    return render(request, 'applications/job_applicants.html', {'job': job, 'applications': applications})


@login_required
def update_application_status(request, app_pk):
    app = get_object_or_404(Application, pk=app_pk)
    if app.job.posted_by != request.user:
        messages.error(request, 'You can only update status for applicants to your jobs.')
        return redirect('jobs:job_list')
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application status updated.')
            return redirect('applications:job_applicants', job_pk=app.job_id)
        else:
            messages.error(request, 'Invalid status.')
    else:
        form = ApplicationStatusForm(instance=app)
    return render(request, 'applications/update_status.html', {'form': form, 'application': app})
