from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import views, status
from rest_framework.exceptions import AuthenticationFailed
from jwt.utils import force_bytes
import jwt
from rest_framework.response import Response
from rest_framework.views import APIView

from Dz_tourism import settings
from user.models import User
from user.serializers import UserSerializer


# Create your views here.



class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email)
        # check existence of email
        if not user:
            return Response("Invalid email or password")

        # check validity of password
        if not user.check_password(password):
            return Response("Invalid email or password")

        if not user.is_staff:
            return Response({"message": "your account not activated"})


        payload={
            'user_id': user.id
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

  
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = User.objects.filter(email=email).first()
        if user is None:
            serializer.save()
            user = User.objects.get(email=email)

            verification_code = get_random_string(length=6)  # Generate a 6-character random code
            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=1),
                'iat': datetime.utcnow(),
                'verification_code': verification_code
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            # Send email with verification code
            self.send_verification_email(email, verification_code)

            response = Response()
            response.set_cookie(key='code', value=token, httponly=True)
            response.data = {
                'message': 'Verification code sent to your email. Please check your inbox and enter the code.'
            }
            return response
        else:
            return Response("User already exists")

    def send_verification_email(self, email, verification_code):  # Add self here
        subject = 'Email Verification Code'
        message = f'Your email verification code is: {verification_code}'
        from_email = 'timibamekki49@gmail.com'  # Replace with your email
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

class VerifyCodeView(APIView):
    def post(self, request):
        code = request.data.get('code')
        token = request.COOKIES.get('code')

        if not code or not token:
            return Response({"message": "Verification code or token missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['user_id']
            verification_code = payload['verification_code']



            if code == verification_code:
                # Code matches, mark email as verified
                try:
                    user = User.objects.get(id=user_id)
                    user.email_verified = True
                    payload = {
                        'user_id': user_id,
                    }
                    user.is_staff = True
                    jwt_token = jwt.encode(payload, 'secret', algorithm='HS256')
                    response = Response()
                    response.set_cookie(key='jwt', value=jwt_token, httponly=True)
                    response.data = {
                        "message": "Email verified successfully.",
                        "jwt": jwt_token
                    }
                    return response
                except ObjectDoesNotExist:
                    return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

