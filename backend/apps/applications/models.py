from django.db import models
from django.conf import settings
from apps.jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = (
        ("APPLIED", "Applied"),
        ("SHORTLISTED", "Shortlisted"),
        ("REJECTED", "Rejected"),
    )

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications' )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='APPLIED'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.candidate.email} → {self.job.title}"
