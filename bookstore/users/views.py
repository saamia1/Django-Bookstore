from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class UserDetailView(generics.RetrieveUpdateAPIView):
    # API endpoint for retrieving and updating user details
    queryset = User.objects.all()  # Queryset for retrieving users
    serializer_class = UserSerializer  # Serializer class for user data
    permission_classes = [IsAuthenticated]  # Permission classes required for endpoint

    def get_object(self):
        # Get the current authenticated user
        return self.request.user
    
class RegisterView(generics.CreateAPIView):
    # API endpoint for user registration
    queryset = User.objects.all()  # Queryset for retrieving users
    serializer_class = UserSerializer  # Serializer class for user data
    permission_classes = []  # No permissions required for registration
    
    def post(self, request, *args, **kwargs):
        # Handle POST request for user registration
        serializer = self.serializer_class(data=request.data)  # Get serializer instance
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return success response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return error response if data is invalid

    def get(self, request, *args, **kwargs):
        # Handle GET request for registration endpoint
        return Response({
            "message": "To register a new user, please send a POST request with the required data."
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)  # Return method not allowed error for GET requests

    def create(self, request, *args, **kwargs):
        # Custom create method to check for existing username
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)  # Return error if username already exists
        return super().create(request, *args, **kwargs)  # Call super create method if username is unique
