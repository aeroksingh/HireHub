from django.urls import path
from .views import apply_job, my_applications, job_applicants, update_application_status
from .views import (
    recruiter_dashboard,
    recruiter_job_applications,
    recruiter_update_status,
)
from . import views

app_name = 'applications'

urlpatterns = [
    path("apply/<int:job_id>/", apply_job, name="apply_job"),
    path("my-applications/", my_applications, name="my_applications"),
    path("job/<int:job_id>/applicants/", job_applicants, name="job_applicants"),
    path(
        "job/<int:job_id>/applications/",
        views.job_applications,
        name="job_applications"
    ),
    path(
        "<int:app_id>/update-status/",
        views.update_application_status,
        name="update_application_status"
    ),

    path("recruiter/dashboard/", recruiter_dashboard, name="recruiter_dashboard"),
    path(
        "recruiter/job/<int:job_id>/applications/",
        recruiter_job_applications,
        name="recruiter_job_applications",
    ),
    path(
        "recruiter/application/<int:app_id>/<str:status>/",
        recruiter_update_status,
        name="recruiter_update_status",
    ),
    # path('job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),  # Duplicate - removed


]

