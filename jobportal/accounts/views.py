from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    """Redirect to role-specific dashboard."""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('accounts:profile_update')
    if profile.is_recruiter:
        return redirect('jobs:recruiter_dashboard')
    return redirect('jobs:job_seeker_dashboard')


@login_required
def profile(request):
    try:
        profile_obj = request.user.profile
    except Profile.DoesNotExist:
        return redirect('accounts:profile_update')
    return render(request, 'accounts/profile.html', {'profile': profile_obj})


@login_required
def profile_update(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user, defaults={'role': 'job_seeker'})
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)
    return render(request, 'accounts/profile_update.html', {'u_form': u_form, 'p_form': p_form})
