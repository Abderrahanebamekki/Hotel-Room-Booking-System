from datetime import datetime, timedelta

from rest_framework import views
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

        user = User.objects.filter(email=email).first()
        # check existence of email
        if not user:
            raise AuthenticationFailed('Invalid email')
        # check validity of password
        if not user.check_password(password):
             raise AuthenticationFailed('Invalid password')

        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload , 'secret', algorithm='HS256')

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
        user_id  = serializer.Meta.fields.index('id')


        payload = {
            'id': user_id,
            'exp': datetime.utcnow() + timedelta(minutes=1),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        serializer.save()
        return response




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

