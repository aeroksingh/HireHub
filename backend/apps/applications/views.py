from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from apps.jobs.models import Job


@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        resume = request.FILES.get('resume')
        application, created = Application.objects.get_or_create(
            candidate=request.user,
            job=job,
            defaults={'resume': resume}
        )

        if created:
            messages.success(request, "Successfully applied for the job.")
        else:
            messages.warning(request, "You have already applied for this job.")
    else:
        # If GET, perhaps redirect or show form, but assuming POST from form
        pass

    return redirect("/")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Application

@login_required
def my_applications(request):
    applications = Application.objects.filter(candidate=request.user)
    applied_applications = applications.filter(status='APPLIED')
    shortlisted_applications = applications.filter(status='SHORTLISTED')
    rejected_applications = applications.filter(status='REJECTED')

    return render(request, "applications/my_applications.html", {
        "applications": applications,
        "applied_applications": applied_applications,
        "shortlisted_applications": shortlisted_applications,
        "rejected_applications": rejected_applications,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from apps.jobs.models import Job


from apps.jobs.views import recruiter_required


@recruiter_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = Application.objects.filter(job=job)

    return render(
        request,
        "applications/job_applications.html",
        {
            "job": job,
            "applications": applications
        }
    )


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Application


@login_required
def update_application_status(request, app_id):
    if request.method != "POST":
        messages.error(request, "Invalid request method")
        return redirect("/")

    # application = get_object_or_404(
    #     Application,
    #     id=app_id,
    #     job__created_by=request.user
    # )
    try:
        application = Application.objects.get(id=app_id)
    except Application.DoesNotExist:
        messages.error(request, "Application not found.")
        return redirect("recruiter_dashboard")

    if application.job.created_by != request.user:
        messages.error(request, "You are not allowed to update this application.")
        return redirect("recruiter_dashboard")


    status = request.POST.get("status")

    if status not in dict(Application.STATUS_CHOICES):
        messages.error(request, "Invalid status")
        return redirect(
            "applications:job_applications",
            job_id=application.job.id
        )

    application.status = status
    application.save()

    if status == "SHORTLISTED":
        send_mail(
            subject="You are shortlisted 🎉",
            message=(
                f"Congratulations!\n\n"
                f"You have been shortlisted for:\n"
                f"{application.job.title}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.candidate.email],
            fail_silently=True,
        )

    messages.success(
        request,
        f"Application marked as {application.get_status_display()}"
    )

    return redirect(
        "applications:job_applications",
        job_id=application.job.id
    )


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from apps.jobs.models import Job
from .models import Application


@staff_member_required
def recruiter_dashboard(request):
    jobs = Job.objects.all()
    return render(
        request,
        "recruiter/dashboard.html",
        {"jobs": jobs}
    )


@staff_member_required
def recruiter_job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = Application.objects.filter(job=job)

    return render(
        request,
        "recruiter/job_applications.html",
        {
            "job": job,
            "applications": applications
        }
    )


@staff_member_required
def recruiter_update_status(request, app_id, status):
    application = get_object_or_404(Application, id=app_id)

    if status in ["SHORTLISTED", "REJECTED"]:
        application.status = status
        application.save()

        if status == "SHORTLISTED":
            send_mail(
                subject="You are shortlisted 🎉",
                message=(
                    f"Congratulations!\n\n"
                    f"You have been shortlisted for:\n"
                    f"{application.job.title}"
                ),
                from_email=None,
                recipient_list=[application.candidate.email],
            )

    messages.success(request, f"Candidate {status}")
    return redirect(
        "applications:recruiter_job_applications",
        job_id=application.job.id
    )


from django.contrib.auth.decorators import login_required
from apps.jobs.models import Job
from apps.jobs.views import recruiter_required


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Application
from apps.jobs.models import Job


@login_required
def job_applications(request, job_id):
    job = get_object_or_404(
        Job,
        id=job_id,
        created_by=request.user  # 🔒 recruiter owns the job
    )

    applications = Application.objects.filter(job=job).select_related("candidate")


    return render(
        request,
        "applications/job_applications.html",
        {
            "job": job,
            "applications": applications
        }
    )
