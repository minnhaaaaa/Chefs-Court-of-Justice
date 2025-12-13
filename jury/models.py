from django.db import models
from django.contrib.auth.models import User
from cases.models import CaseSubmission

class JuryVote(models.Model):
    VOTE_CHOICES = [
        ('GUILTY', 'Guilty'),
        ('NOT_GUILTY', 'Not Guilty'),
    ]

    case = models.ForeignKey(CaseSubmission, on_delete=models.CASCADE)
    juror = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.CharField(max_length=20, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('case', 'juror')
        
    def __str__(self):
        return f"{self.juror.username} - {self.case.title}"


   
