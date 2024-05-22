from datetime import datetime, timedelta

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views, status
from rest_framework.exceptions import AuthenticationFailed
from jwt.utils import force_bytes
import jwt
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from Dz_tourism import settings
from user.models import User
from user.serializers import UserSerializer


# Create your views here.


class LoginView(APIView):
    def post(self, request):
        email = request.data['username']
        password = request.data['password']

        user = User.objects.get(username=email)
        # check existence of email
        if not user:
            return Response("Invalid email or password", status=status.HTTP_404_NOT_FOUND)

        if not user.is_active :
            return Response("Inactive account", status=status.HTTP_404_NOT_FOUND)

        # check validity of password
        if not user.check_password(password):
            return Response("Invalid email or password", status=status.HTTP_404_NOT_FOUND)

        payload = {
            'user_id': user.id
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response(status=status.HTTP_200_OK)

        response.data = {
            'message': "successfully login" ,
            'auth':token
        }
        return response


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('username')
        name = serializer.validated_data.get('name')
        password = serializer.validated_data.get('password')
        user = User.objects.filter(username=email).first()
        response = Response()
        if user is None:
            # serializer.save()
            # user = User.objects.get(email=email)

            verification_code = get_random_string(length=6)  # Generate a 6-character random code
            payload = {
                'email': email,
                'name': name,
                'password': password,
                'exp': datetime.utcnow() + timedelta(minutes=10),
                'iat': datetime.utcnow(),
                'verification_code': verification_code
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            # Send email with verification code
            self.send_verification_email(email, verification_code)


            response.data = {
                'message': 'Verification code sent to your email. Please check your inbox and enter the code.',
                'code': token
            }
            return response
        else:
            response.data = {
                'message': "User already exists"
            }
            return response

    def send_verification_email(self, email, verification_code):  # Add self here
        subject = 'Email Verification Code'
        message = f'Your email verification code is: {verification_code}'
        from_email = 'timibamekki49@gmail.com'  # Replace with your email
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)


class VerifyCodeView(APIView):
    def post(self, request):
        code = request.query_params.get('code')
        token = request.headers.get('Authorization').split(' ')[1]

        if not code or not token:
            return Response({"message": "Verification code or token missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            email = payload['email']
            name = payload['name']
            password = payload['password']
            verification_code = payload['verification_code']

            if code == verification_code:
                # Code matches, mark email as verified
                user = User.objects.create_user(username=email, password=password, name=name)
                user.email_verified = True
                user.save()

                user_id = user.id
                payload = {'user_id': user_id}
                jwt_token = jwt.encode(payload, 'secret', algorithm='HS256')
                return Response({"message": "Email verified successfully.", "auth": jwt_token}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):

    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({"message": "Authorization header missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['user_id']).first()

        if not user:
            return Response({'message': 'Admin not found!'}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_staff:  # Check if the user is an admin
            return Response({'message': 'Forbidden!'}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class ActivateView(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({"message": "Authorization header missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['user_id']).first()

        if not user:
            return Response({'message': 'Admin not found!'}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_staff:  # Check if the user is an admin
            return Response({'message': 'Forbidden!'}, status=status.HTTP_403_FORBIDDEN)

        user = User.objects.get(id=id)
        if not user :
            return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = not user.is_active
        user.save()
        return Response(data={'message': 'success'}, status=status.HTTP_200_OK)


# class ResendCode(APIView):
#     def post(self, request):
#         token = request.COOKIES.get('code')
#
#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#             user_id = payload['user_id']
#             # Check if token has expired
#             current_time = datetime.utcnow()
#             expiration_time = datetime.fromtimestamp(payload['exp'])
#             if current_time > expiration_time:
#                 # Token has expired, return an error response
#                 return Response({"message": "Token has expired. Please request a new verification code."}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({"message": "Token is still valid."}, status=status.HTTP_200_OK)
#         except jwt.InvalidTokenError:
#             return Response({"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
#
#     def send_verification_email(self, email, verification_code):
#         subject = 'Email Verification Code'
#         message = f'Your email verification code is: {verification_code}'
#         from_email = 'timibamekki49@gmail.com'
#         recipient_list = [email]
#         send_mail(subject, message, from_email, recipient_list)


class ForgetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('username')
        user = User.objects.get(username=email)
        if user:
            # Construct password reset link
            reset_link = request.build_absolute_uri(
                f"http://localhost:3000/changePasswordPage"
            )
            # Send email
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', {
                'reset_link': reset_link
            })
            text_content = strip_tags(message)
            email_content = EmailMultiAlternatives(subject, text_content, 'timibamekki49@gmail.com', [email])
            email_content.attach_alternative(message, 'text/html')  # Set content type to HTML
            email_content.send()
            return Response({'message': 'Password reset link has been sent to your email.', "id_user": user.id}, status=status.HTTP_200_OK)
        else:
            # Handle case where email doesn't exist
            return Response({'error': 'Email does not exist'}, status=status.HTTP_404_NOT_FOUND)


# class ResetPasswordView(APIView):
#     def get(self, request , user_id):
#         user = User.objects.get(id=user_id)
#         if user:
#             token = default_token_generator.make_token(user)
#             response = Response()
#             response.set_cookie(key='reset', value=token, httponly=True)
#             return response
#         else:
#             return Response({'error': 'user not exist'}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(APIView):
    def post(self, request):
        user_id = request.data['id']
        user = User.objects.get(id=user_id)
        new_password = request.data['password']
        if user:
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'user not exist'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
