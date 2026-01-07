from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('CANDIDATE', 'Candidate'),
        ('RECRUITER', 'Recruiter'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CANDIDATE')

    def __str__(self):
        return self.email
