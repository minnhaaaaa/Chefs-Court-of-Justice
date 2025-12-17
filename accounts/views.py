from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer

VALID_ROLES = ['DEFENDANT', 'PLAINTIFF', 'JUROR', 'JUDGE']

@api_view(['POST'])
def signup(request):
    user_serializer = UserSerializer(data=request.data)

    if not user_serializer.is_valid():
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = user_serializer.validated_data['username']

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = user_serializer.save()
    role = request.data.get('role')

    VALID_ROLES = ['DEFENDANT', 'PLAINTIFF', 'JUROR', 'JUDGE']
    if role not in VALID_ROLES:
        return Response(
            {"error": "Invalid role"},
            status=status.HTTP_400_BAD_REQUEST
        )

    Profile.objects.get_or_create(user=user, role=role)

    return Response(
        {"message": "User created successfully"},
        status=status.HTTP_201_CREATED
    )