from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse
from apps.jobs.models import Job
from apps.applications.models import Application

def recruiter_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to access the recruiter dashboard.")
            return redirect('accounts:login')
        if request.user.role != 'RECRUITER':
            messages.error(request, "You are not authorized to access this page.")
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper

@recruiter_required
def dashboard(request):
    jobs = Job.objects.filter(created_by=request.user)
    total_jobs = jobs.count()
    total_applications = Application.objects.filter(job__in=jobs).count()
    context = {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'jobs': jobs,
    }
    return render(request, 'recruiter/dashboard.html', context)

@recruiter_required
def jobs(request):
    jobs = Job.objects.filter(created_by=request.user)
    context = {
        'jobs': jobs,
    }
    return render(request, 'recruiter/jobs.html', context)

@recruiter_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, created_by=request.user)
    applications = Application.objects.filter(job=job)
    context = {
        'job': job,
        'applications': applications,
    }
    return render(request, 'recruiter/applicants.html', context)

@recruiter_required
def update_application_status(request, application_id, status):
    application = get_object_or_404(Application, id=application_id, job__created_by=request.user)
    if status in ['SHORTLISTED', 'REJECTED']:
        application.status = status
        application.save()
        messages.success(request, f"Application status updated to {status}.")
    return redirect('recruiter:dashboard')

# recruiter/views.py
@login_required
def recruiter_jobs(request):
    jobs = Job.objects.filter(created_by=request.user)
    return render(request, "recruiter/jobs.html", {"jobs": jobs})

