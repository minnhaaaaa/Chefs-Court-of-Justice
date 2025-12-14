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
    
class Vote(models.Model):
    VOTE_CHOICES = [
        ('GUILTY', 'Guilty'),
        ('NOT_GUILTY', 'Not Guilty'),
    ]
    case = models.ForeignKey('CaseSubmission', on_delete=models.CASCADE, related_name='votes')
    juror = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.CharField(max_length=20, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('case', 'juror')

    def __str__(self):
        return f"{self.juror.username} voted {self.vote} for case {self.case.title}"

