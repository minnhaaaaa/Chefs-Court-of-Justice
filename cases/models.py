from django.db import models
from django.contrib.auth.models import User

class CaseSubmission(models.Model):
    PARTY_CHOICES = [
        ('DEFENDANT', 'Defendant'),
        ('PLAINTIFF', 'Plaintiff'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
   
    title = models.CharField(max_length=255)
    argument_text = models.TextField()
    evidence_file = models.FileField(upload_to='evidence/', null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    party_type = models.CharField(max_length=20, choices=PARTY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

