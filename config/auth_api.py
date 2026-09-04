from typing import cast

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        assert type(request.data) == dict, "request.data should be a dictionary"
        username = request.data.get('username', '').strip()
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '')

        if not username or not password:
            return Response(
                {'detail': 'username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {'detail': 'A user with this username already exists.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request._request, user)
        return Response({'id': user.pk, 'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        assert type(request.data) == dict, "request.data should be a dictionary"
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')
        user = cast(User | None, authenticate(request=request._request, username=username, password=password))
        if user is None:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        login(request._request, user)
        return Response({'id': user.pk, 'username': user.username, 'email': user.email})


class LogoutView(APIView):
    def post(self, request: Request) -> Response:
        logout(request._request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        assert type(request.data) == dict, "request.data should be a dictionary"
        form = PasswordResetForm({'email': request.data.get('email', '').strip()})
        if form.is_valid():
            form.save(
                request=request._request,
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.txt',
                subject_template_name='registration/password_reset_subject.txt',
            )
        return Response({'detail': 'If an account exists, a reset email has been sent.'})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, uidb64: str, token: str) -> Response:
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is None or not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid or expired reset link.'}, status=status.HTTP_400_BAD_REQUEST)
        assert type(request.data) == dict, "request.data should be a dictionary"
        password = request.data.get('password', '')
        try:
            user.set_password(password)
            user.full_clean(exclude=['password'])
        except ValidationError as error:
            return Response({'detail': error.messages}, status=status.HTTP_400_BAD_REQUEST)
        user.save(update_fields=['password'])
        return Response({'detail': 'Password has been reset.'})
