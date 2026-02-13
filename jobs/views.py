from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

from .models import Job
from .forms import JobForm
from accounts.models import Profile


def job_list(request):
    jobs = Job.objects.all()
    # Search by title
    query = request.GET.get('q', '').strip()
    if query:
        jobs = jobs.filter(title__icontains=query)
    # Filter by location
    location = request.GET.get('location', '').strip()
    if location:
        jobs = jobs.filter(location__icontains=location)
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'jobs/job_list.html', {
        'page_obj': page_obj,
        'query': query,
        'location': location,
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = job.application_set.filter(applicant=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'has_applied': has_applied})


@login_required
def job_create(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('accounts:profile_update')
    if not profile.is_recruiter:
        messages.error(request, 'Only recruiters can post jobs.')
        return redirect('jobs:job_list')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('jobs:job_detail', pk=job.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Post a Job'})


@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.posted_by != request.user:
        messages.error(request, 'You can only edit your own jobs.')
        return redirect('jobs:job_list')
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('jobs:job_detail', pk=job.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'job': job, 'title': 'Edit Job'})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.posted_by != request.user:
        messages.error(request, 'You can only delete your own jobs.')
        return redirect('jobs:job_list')
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('jobs:recruiter_dashboard')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


@login_required
def recruiter_dashboard(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('accounts:profile_update')
    if not profile.is_recruiter:
        messages.error(request, 'Access denied. Recruiter only.')
        return redirect('jobs:job_list')
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'jobs/recruiter_dashboard.html', {'jobs': jobs})


@login_required
def job_seeker_dashboard(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('accounts:profile_update')
    if not profile.is_job_seeker:
        messages.error(request, 'Access denied. Job seeker only.')
        return redirect('jobs:job_list')
    from applications.models import Application
    applications = Application.objects.filter(applicant=request.user).select_related('job')
    return render(request, 'jobs/job_seeker_dashboard.html', {'applications': applications})
