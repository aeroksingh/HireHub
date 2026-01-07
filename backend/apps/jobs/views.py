from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse
from .models import Job
from apps.applications.models import Application

def recruiter_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to access this feature.")
            return redirect('accounts:login')
        if request.user.role != 'RECRUITER':
            messages.error(request, "You are not authorized to access this page.")
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper

def job_list(request):
    jobs = Job.objects.all()

    applied_jobs = []
    if request.user.is_authenticated:
        applied_jobs = Application.objects.filter(
            candidate=request.user
        ).values_list("job_id", flat=True)

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs,
            "applied_jobs": applied_jobs
        }
    )

@recruiter_required
def post_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        Job.objects.create(
            title=title,
            description=description,
            location=location,
            job_type=job_type,
            created_by=request.user
        )
        messages.success(request, "Job posted successfully!")
        return redirect('jobs:job-list')
    return render(request, 'jobs/post_job.html')


from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Job

@login_required
def recruiter_dashboard(request):
    jobs = Job.objects.filter(created_by=request.user).annotate(
        applicants_count=Count('applications')
    )

    return render(request, 'jobs/job_list.html', {'jobs': jobs})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job


@login_required
def delete_job(request, job_id):
    if request.method != "POST":
        messages.error(request, "Invalid request")
        return redirect("recruiter:jobs")

    job = get_object_or_404(
        Job,
        id=job_id,
        created_by=request.user  # 🔒 recruiter ownership check
    )

    job.delete()
    messages.success(request, "Job deleted successfully")

    return redirect("recruiter:jobs")
