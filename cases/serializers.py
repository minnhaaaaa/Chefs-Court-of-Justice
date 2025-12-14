from rest_framework import serializers
from .models import CaseSubmission

class CaseSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseSubmission
        fields = [
            'id',
            'title',
            'argument_text',
            'evidence_file',
            'party_type',
            'status',
            'created_at'
        ]
        read_only_fields = ['status', 'created_at']
