import random
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import EmailConfirmationCode
from .serializers import UserAuthSerializer, UserRegisterSerializer


def generate_confirmation_code():
    return str(random.randint(100000, 999999))

def send_confirmation_code(user, code):
    subject = "Email confirmation"
    message = f"Your confirmation code is: {code}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

# @api_view(['POST'])
# def authorization_api_view(request):
#     serializer = UserAuthSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if not user.is_active:
#             return Response(data={"detail": "Please confirm your email first."}, status=status.HTTP_401_UNAUTHORIZED)
#         try:
#             token = Token.objects.get(user=user)
#         except Token.DoesNotExist:
#             token = Token.objects.create(user=user)
#         return Response(data={'key': token.key})
#     return Response(status=status.HTTP_401_UNAUTHORIZED)

class AuthorizationAPIView(GenericAPIView):
    serializer_class = UserAuthSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                return Response(data={"detail": "Please confirm your email first."}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['POST'])
# def registration_api_view(request):
#     serializer = UserRegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']
#         email = serializer.validated_data['email']
#         user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
#         code = generate_confirmation_code()
#         EmailConfirmationCode.objects.update_or_create(user=user, defaults={'code': code})
#         send_confirmation_code(user, code)
#         return Response(
#             data={"user_id": user.id, "detail": "Check your email for the confirmation code."},
#             status=status.HTTP_201_CREATED,
#         )
#     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationAPIView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
            code = generate_confirmation_code()
            EmailConfirmationCode.objects.update_or_create(user=user, defaults={'code': code})
            send_confirmation_code(user, code)
            return Response(
                data={"user_id": user.id, "detail": "Check your email for the confirmation code."},
                status=status.HTTP_201_CREATED,
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def confirm_email_api_view(request):
#     code = request.data.get('code')
#     if not code:
#         return Response(data={"detail": "Code is required."}, status=status.HTTP_400_BAD_REQUEST)
#     try:
#         confirmation = EmailConfirmationCode.objects.select_related('user').get(code=code)
#     except EmailConfirmationCode.DoesNotExist:
#         return Response(data={"detail": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)
#     user = confirmation.user
#     user.is_active = True
#     user.save(update_fields=['is_active'])
#     confirmation.delete()
#     return Response(data={"detail": "Email confirmed successfully."}, status=status.HTTP_200_OK)

class ConfirmEmailAPIView(GenericAPIView):
    serializer_class = UserAuthSerializer
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response(data={"detail": "Code is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            confirmation = EmailConfirmationCode.objects.select_related('user').get(code=code)
        except EmailConfirmationCode.DoesNotExist:
            return Response(data={"detail": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)
        user = confirmation.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        confirmation.delete()
        return Response(data={"detail": "Email confirmed successfully."}, status=status.HTTP_200_OK)
