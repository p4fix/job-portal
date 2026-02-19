from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

from .models import Job, SavedJob
from .forms import JobForm
from accounts.models import Profile


def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    # Search by title or company
    query = request.GET.get('q', '').strip()
    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(company_name__icontains=query))
    # Filter by location
    location = request.GET.get('location', '').strip()
    if location:
        jobs = jobs.filter(location__icontains=location)
    # Filter by category
    category = request.GET.get('category', '').strip()
    if category:
        jobs = jobs.filter(category=category)
    # Filter by job type
    job_type = request.GET.get('job_type', '').strip()
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    # Filter by experience level
    experience = request.GET.get('experience', '').strip()
    if experience:
        jobs = jobs.filter(experience_level=experience)
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'jobs/job_list.html', {
        'page_obj': page_obj,
        'query': query,
        'location': location,
        'category': category,
        'job_type': job_type,
        'experience': experience,
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    is_saved = False
    if request.user.is_authenticated:
        has_applied = job.application_set.filter(applicant=request.user).exists()
        is_saved = job.saved_by_users.filter(user=request.user).exists()
    # Get related jobs (same category)
    related_jobs = Job.objects.filter(category=job.category, is_active=True).exclude(pk=job.pk)[:5]
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied,
        'is_saved': is_saved,
        'related_jobs': related_jobs,
    })


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
    from applications.models import Application
    total_applications = Application.objects.filter(job__posted_by=request.user).count()
    pending_applications = Application.objects.filter(job__posted_by=request.user, status='Pending').count()
    accepted_applications = Application.objects.filter(job__posted_by=request.user, status='Accepted').count()
    active_jobs = jobs.filter(is_active=True).count()
    return render(request, 'jobs/recruiter_dashboard.html', {
        'jobs': jobs,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'accepted_applications': accepted_applications,
        'active_jobs': active_jobs,
        'total_jobs': jobs.count(),
    })


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
    from .models import SavedJob
    applications = Application.objects.filter(applicant=request.user).select_related('job')
    saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job')
    total_applications = applications.count()
    pending_applications = applications.filter(status='Pending').count()
    accepted_applications = applications.filter(status='Accepted').count()
    return render(request, 'jobs/job_seeker_dashboard.html', {
        'applications': applications[:5],
        'saved_jobs': saved_jobs[:5],
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'accepted_applications': accepted_applications,
        'saved_count': saved_jobs.count(),
    })


@login_required
def save_job(request, pk):
    """Save/bookmark a job"""
    job = get_object_or_404(Job, pk=pk)
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('accounts:profile_update')
    if not profile.is_job_seeker:
        messages.error(request, 'Only job seekers can save jobs.')
        return redirect('jobs:job_detail', pk=pk)
    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if created:
        messages.success(request, 'Job saved successfully.')
    else:
        messages.info(request, 'Job already saved.')
    return redirect('jobs:job_detail', pk=pk)


@login_required
def unsave_job(request, pk):
    """Remove a saved job"""
    job = get_object_or_404(Job, pk=pk)
    SavedJob.objects.filter(user=request.user, job=job).delete()
    messages.success(request, 'Job removed from saved list.')
    return redirect('jobs:job_detail', pk=pk)


@login_required
def saved_jobs_list(request):
    """View all saved jobs"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('accounts:profile_update')
    if not profile.is_job_seeker:
        messages.error(request, 'Access denied.')
        return redirect('jobs:job_list')
    saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job')
    return render(request, 'jobs/saved_jobs.html', {'saved_jobs': saved_jobs})
