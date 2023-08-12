from rest_framework import serializers
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication.jwt_authentication import JWTAuthentication
from courses.api.serializer import AuthorSerializer, StudentSerializer
from .models import Author, Student, User
from django.core.cache import cache
import json


def return_all_data_with_cache(request, cache_key: str, user_model_name: str,
                               serializer_class: serializers.ModelSerializer):
    data = cache.get(key=cache_key)
    if data:
        data = json.loads(data)
        return Response(data=data, status=status.HTTP_200_OK)

    jwt_authenticator = JWTAuthentication(user_model_name, request.data)
    jwt_response, payload = jwt_authenticator.authenticate(request)

    if jwt_response is None:
        return Response({'message': 'Not Authenticated'}, status=status.HTTP_204_NO_CONTENT)

    serializer = serializer_class(Author.objects.all(), many=True)
    data = serializer.data
    cache.set(key=cache_key, value=json.dumps(data))

    return data


# Create your views here.
class CreateAuthorAPIView(APIView):
    # permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = AuthorSerializer(data=user)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({'message': 'User created successfully'},
                        status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username, password=password)

        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('User not found')

        jwt_authentication = JWTAuthentication("User", request.data)

        jwt_token = jwt_authentication.create_jwt()

        response = Response()

        response.set_cookie(key='jwt', value=jwt_token, httponly=True)
        response.status_code(status.HTTP_200_OK)

        return response


class AuthorRetrieveUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.author)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('author', {})
        serializer = AuthorSerializer(
            request.author, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ObtainAuthorTokenView(APIView):

    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        jwt_request = request.data
        author = Author.objects.filter(email=jwt_request.get("data"))
        jwt_authentication_request = JWTAuthentication("Author", author, token=token)
        response, payload = jwt_authentication_request.authenticate(request=request)

        return Response({'message': 'Authenticated', 'body': response}, status=status.HTTP_202_ACCEPTED)


class ObtainAuthorsView(PermissionRequiredMixin, APIView):
    permission_required = 'courses.author.view_author'
    serializer_class = AuthorSerializer

    def get(self, request):
        data = return_all_data_with_cache(request, "author", 'Author', serializer_class=self.serializer_class)
        return Response(data, status=status.HTTP_200_OK)


class ObtainStudentsView(APIView):
    serializer_class = StudentSerializer

    def get(self, request):
        data = return_all_data_with_cache(request, "student", 'Student', serializer_class=self.serializer_class)
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def authenticate_author(request):
    jwt_authentication = JWTAuthentication('Author')
    response = jwt_authentication.authenticate(request=request)

    return Response({'message': 'Authenticated', 'body': response}, status=status.HTTP_202_ACCEPTED)


def autenticate_user(user, request):
    # try:
    #     if user:
    #         try:
    #             payload = jwt_payload_handler(user)
    #             token = jwt.encode(payload, settings.SECRET_KEY)
    #             user_details = {'name': "%s %s" % (
    #                 user.first_Name, user.last_Name), 'token': token}
    #             user_logged_in.send(sender=user.__class__,
    #                                 request=request, user=user)
    #             return Response(user_details, status=status.HTTP_200_OK)
    #         except Exception as e:
    #             raise e
    #     else:
    #         res = {
    #             'error': 'can not authenticate with the given credentials or the account has been deactivated'}
    #         return Response(res, status=status.HTTP_403_FORBIDDEN)
    # except KeyError:
    res = {'error': 'please provide a email and a password'}
    return Response(res)
