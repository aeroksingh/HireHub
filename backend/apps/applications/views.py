from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Application
from apps.jobs.models import Job
from apps.jobs.views import recruiter_required


# =========================
# Candidate: Apply for job
# =========================
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        resume = request.FILES.get("resume")

        application, created = Application.objects.get_or_create(
            candidate=request.user,
            job=job,
            defaults={"resume": resume},
        )

        if created:
            messages.success(request, "Successfully applied for the job.")
        else:
            messages.warning(request, "You have already applied for this job.")

    return redirect("/")


# =========================
# Candidate: My applications
# =========================
@login_required
def my_applications(request):
    applications = Application.objects.filter(candidate=request.user)

    return render(
        request,
        "applications/my_applications.html",
        {
            "applications": applications,
            "applied_applications": applications.filter(status="APPLIED"),
            "shortlisted_applications": applications.filter(status="SHORTLISTED"),
            "rejected_applications": applications.filter(status="REJECTED"),
        },
    )


# =========================
# Recruiter: View applicants
# =========================
@recruiter_required
def job_applicants(request, job_id):
    job = get_object_or_404(
        Job,
        id=job_id,
        created_by=request.user,  # 🔒 recruiter owns job
    )

    applications = (
        Application.objects
        .filter(job=job)
        .select_related("candidate")
    )

    return render(
        request,
        "applications/job_applications.html",
        {
            "job": job,
            "applications": applications,
        },
    )


# =========================
# Recruiter: Update status (SAFE)
# =========================
@login_required
def update_application_status(request, app_id):
    if request.method != "POST":
        messages.error(request, "Invalid request.")
        return redirect("/")

    application = get_object_or_404(
        Application,
        id=app_id,
        job__created_by=request.user,  # 🔒 recruiter owns job
    )

    status = request.POST.get("status")

    if status not in dict(Application.STATUS_CHOICES):
        messages.error(request, "Invalid status.")
        return redirect(
            "applications:job_applications",
            job_id=application.job.id,
        )

    application.status = status
    application.save(update_fields=["status"])

    # ❌ IMPORTANT:
    # DO NOT send email here on Render Free
    # Email inside request causes 502 timeouts

    messages.success(
        request,
        f"Application marked as {application.get_status_display()}",
    )

    return redirect(
        "applications:job_applications",
        job_id=application.job.id,
    )
