from datetime import datetime

import jwt
from django.conf import settings
from django.core.exceptions import FieldError
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError
from django.apps import apps

from courses.Exceptions.Exceptions import TypeErrorException, FieldErrorException, LookUpError, \
    AttributeErrorException


class JWTAuthentication(authentication.BaseAuthentication):

    def __init__(self, user_model_name='Author', user_class=None):
        self.user_model_name = user_model_name
        self.user_class = user_class

    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = self.get_the_token_from_header(jwt_token)

        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Invalid Signature')
        except:
            raise ParseError()

        username = payload.get('user_identifier')

        course_model = 'courses.' + self.user_model_name

        try:
            course_model = apps.get_model(course_model, require_ready=False)

            authenticated_object = course_model.objects.filter(email=username, password=request.data.get('password'))

        except TypeError as e:
            raise TypeErrorException(str(e))

        except FieldError as e:
            raise FieldErrorException(str(e))

        except LookupError as error:
            raise LookUpError(str(error))

        except AttributeError as error:
            raise AttributeErrorException(str(error))

        if authenticated_object is None:
            raise AuthenticationFailed("User not found")

        return authenticated_object, payload

    def create_jwt(self):
        payload = {
            'user_identifier': self.user_class.get('email'),
            'exp': int((datetime.now() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA']).timestamp()),
            # set the expiration time for 5 hour from now
            'iat': datetime.now().timestamp(),
            'username': self.user_class.get('email'),
        }

        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    def get_the_token_from_header(self, token):
        token = token.replace('Bearer', '').replace('', '')
        return token

    def generate_refresh_token(self):
        refresh_token_payload = {
            'user_identifier': self.user_class.get('email'),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        }
        refresh_token = jwt.encode(
            refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256').decode('utf-8')

        return refresh_token
