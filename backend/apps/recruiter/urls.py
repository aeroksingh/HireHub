from django.urls import path
from . import views

app_name = 'recruiter'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobs/', views.jobs, name='jobs'),
    path('job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path("jobs/", views.recruiter_jobs, name="jobs"),
    path("job/<int:job_id>/applicants/", views.job_applicants, name="job_applicants"),
    path('application/<int:application_id>/update/<str:status>/', views.update_application_status, name='update_application_status'),
]