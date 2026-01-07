from django.urls import path
from .views import job_list, post_job
from . import views
app_name = 'jobs'

urlpatterns = [
    path("", job_list, name="job-list"),
    path("post/", post_job, name="post_job"),
    path(
        "delete/<int:job_id>/",
        views.delete_job,
        name="delete_job"
    ),
    path("delete/<int:job_id>/", views.delete_job, name="delete_job"),
    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
]

