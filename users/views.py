from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from six import text_type

from subletshark import settings
from .serializers import UserSerializer


class VerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)


token_generator = VerificationTokenGenerator()
password_reset_token_generator = PasswordResetTokenGenerator()


class EmailVerificationView(generics.UpdateAPIView):
    permission_classes = [AllowAny, ]

    def patch(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if not token_generator.check_token(user, token):
                # User has already used the token.
                return Response(status=HTTP_400_BAD_REQUEST, data={'detail': 'checking token failed'})
            if user.is_active:
                # Do nothing?
                return Response(status=HTTP_400_BAD_REQUEST, data={'detail': 'user already activated'})
            else:
                user.is_active = True
                user.save()
        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND, data={'detail': 'user not found.'})

        return Response(status=HTTP_204_NO_CONTENT)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        email = request.data['email']

        try:
            validate_email(email)
        except ValidationError as exc:
            return Response(status=HTTP_400_BAD_REQUEST, data=exc.message)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={'detail': 'user account with that email does not exist.'}
            )
        domain = settings.FRONTEND_URL
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = password_reset_token_generator.make_token(user)
        link = f'{uidb64}/{token}'
        activate_url = f'http://{domain}/auth/reset-password/{link}'
        email_body = f'Hi {user.first_name}, we received a request to reset your Sublet Shark ' \
                     f'password. Please use this link to reset the password for your account.\n' \
                     f'{activate_url}\n\nIf you did not issue this request, ignore this email.' \
                     f'\n\nThanks,\nSublet Shark'
        email = EmailMessage(
            'Reset your Sublet Shark password',
            email_body,
            to=[user.email],
        )
        email.send()
        return Response(status=HTTP_204_NO_CONTENT)

    def patch(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if not password_reset_token_generator.check_token(user, token):
                # User has already used the token.
                return Response(status=HTTP_400_BAD_REQUEST, data={'detail': 'checking token failed.'})
            else:
                password = request.data['password']
                password2 = request.data['password2']
                if password != password2:
                    return Response(status=HTTP_400_BAD_REQUEST, data={'detail': 'passwords do not match.'})
                user.set_password(password)
                user.save()
        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND, data={'detail': 'user not found.'})

        return Response(status=HTTP_204_NO_CONTENT)


class RegisterView(generics.CreateAPIView):
    """View for registering a new user."""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        user = User.objects.get(email=response.data['email'])
        user.is_active = False
        user.save()
        domain = settings.FRONTEND_URL
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        link = f'{uidb64}/{token}'
        activate_url = f'http://{domain}/auth/activate/{link}'
        email_body = f'Hi {user.first_name}, please use this link to activate your account.\n' \
                     f'{activate_url}\n\nThanks,\nSublet Shark'
        email = EmailMessage(
            'Activate your account with Sublet Shark',
            email_body,
            to=[user.email],
        )
        email.send()
        return response


class BlacklistTokenView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
