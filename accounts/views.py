import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import (
    RegisterSerializer, UserSerializer, PasswordChangeSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser

# 1) Register endpoint
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    # CreateAPIView handles POST -> create

# 2) Custom TokenObtainPairView to include user info in response
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # custom claims (agar kerak bo'lsa)
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # qo'shimcha user ma'lumotlarini qaytarish
        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
            }
        })
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

# 3) Logout (blacklist refresh token)
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# 4) User Profile endpoints
class ProfileView(APIView):
    """
    Get, update user profile.
    GET: Retrieve current user profile
    PUT: Full update of user profile
    PATCH: Partial update of user profile
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get current user profile information.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Full update of user profile.
        """
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        Partial update of user profile.
        """
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 5) Password Change endpoint
class ChangePasswordView(APIView):
    """
    Change user password.
    Requires old password verification and new password validation.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Change user password.
        Requires: old_password, new_password, new_password2
        """
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password changed successfully."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 6) Password Reset endpoints
class PasswordResetView(APIView):
    """
    Send password reset link to user's email.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Send password reset email.
        Requires: email
        """
        # Handle both JSON and form data
        # DRF's request.data should work, but handle edge cases
        data = request.data
        if not data or (isinstance(data, dict) and not data):
            # Try to get from body if request.data is empty
            if hasattr(request, 'body') and request.body:
                try:
                    data = json.loads(request.body)
                except (json.JSONDecodeError, ValueError):
                    data = {}
        
        serializer = PasswordResetSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid request", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            # Generate token
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset link
            # In production, replace with your frontend URL
            reset_link = f"{request.scheme}://{request.get_host()}/api/auth/password-reset-confirm/?uid={uid}&token={token}"
            
            # Send email
            subject = 'Password Reset Request'
            message = f'''
Hello {user.username or user.email},

You requested a password reset for your account.

Please click the following link to reset your password:
{reset_link}

If you did not request this, please ignore this email.

This link will expire in 24 hours.

Best regards,
JWT Auth Team
'''
            from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@example.com'
            
            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log error but don't reveal to user
                return Response(
                    {"message": "Failed to send email. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Always return success message for security (don't reveal if email exists)
            return Response(
                {"message": "If an account with this email exists, a password reset link has been sent."},
                status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            # Don't reveal if email exists or not for security
            return Response(
                {"message": "If an account with this email exists, a password reset link has been sent."},
                status=status.HTTP_200_OK
            )


class PasswordResetConfirmView(APIView):
    """
    Confirm password reset with token and set new password.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Reset password with token.
        Requires: uid, token, new_password, new_password2
        """
        # Handle both JSON and form data
        # DRF's request.data should work, but handle edge cases
        data = request.data
        if not data or (isinstance(data, dict) and not data):
            # Try to get from body if request.data is empty
            if hasattr(request, 'body') and request.body:
                try:
                    data = json.loads(request.body)
                except (json.JSONDecodeError, ValueError):
                    data = {}
        
        serializer = PasswordResetConfirmSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password has been reset successfully."},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Invalid request", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
