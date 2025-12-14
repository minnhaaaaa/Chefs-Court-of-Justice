from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CaseSubmission
from .models import Vote
from .serializers import CaseSubmissionSerializer
from accounts.permissions import IsDefendantOrPlaintiff, IsJuror, IsJudge


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDefendantOrPlaintiff])
def submit_case(request):
    serializer = CaseSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(submitted_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsJuror])
def view_approved_cases(request):
    cases = CaseSubmission.objects.filter(status='APPROVED')
    serializer = CaseSubmissionSerializer(cases, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsJuror])
def vote_case(request, case_id):
    case = get_object_or_404(CaseSubmission, id=case_id, status='APPROVED')
    juror = request.user
    vote_value = request.data.get('vote')

    if vote_value not in ['GUILTY', 'NOT_GUILTY']:
        return Response({'error': 'Invalid vote. Must be GUILTY or NOT_GUILTY'},
                        status=status.HTTP_400_BAD_REQUEST)

    vote_obj, created = Vote.objects.get_or_create(case=case, juror=juror, defaults={'vote': vote_value})
    if not created:
        return Response({'error': 'You have already voted for this case'},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': f'Vote recorded as {vote_value}'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsJuror])
def vote_results(request, case_id):
    case = get_object_or_404(CaseSubmission, id=case_id)
    votes = Vote.objects.filter(case=case)
    guilty_count = votes.filter(vote='GUILTY').count()
    not_guilty_count = votes.filter(vote='NOT_GUILTY').count()
    return Response({
        'case': case.title,
        'guilty_votes': guilty_count,
        'not_guilty_votes': not_guilty_count
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsJudge])
def judge_view_all(request):
    """View all case submissions"""
    cases = CaseSubmission.objects.all().order_by('-created_at')
    serializer = CaseSubmissionSerializer(cases, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsJudge])
def edit_case(request, case_id):
    """Edit case details"""
    case = get_object_or_404(CaseSubmission, id=case_id)
    # Update only allowed fields
    for field in ['title', 'argument_text', 'party_type']:
        if field in request.data:
            setattr(case, field, request.data[field])
    case.save()
    serializer = CaseSubmissionSerializer(case)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsJudge])
def approve_case(request, case_id):
    """Approve case"""
    case = get_object_or_404(CaseSubmission, id=case_id)
    case.status = 'APPROVED'
    case.save()
    serializer = CaseSubmissionSerializer(case)
    return Response({"message": "Case approved", "case": serializer.data})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsJudge])
def reject_case(request, case_id):
    """Reject case"""
    case = get_object_or_404(CaseSubmission, id=case_id)
    case.status = 'REJECTED'
    case.save()
    serializer = CaseSubmissionSerializer(case)
    return Response({"message": "Case rejected", "case": serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsJudge])
def delete_case(request, case_id):
    """Delete case"""
    case = get_object_or_404(CaseSubmission, id=case_id)
    case.delete()
    return Response({"message": "Case deleted"})
