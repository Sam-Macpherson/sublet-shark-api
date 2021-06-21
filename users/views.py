from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework_simplejwt.tokens import RefreshToken
from six import text_type

from subletshark import settings
from .serializers import UserSerializer


class VerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)


token_generator = VerificationTokenGenerator()


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
                     f'{activate_url}'
        email = EmailMessage(
            'Activate your account with Sublet Shark',
            email_body,
            'sam.macpherson15@gmail.com',
            [user.email],
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
