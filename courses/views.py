from django.contrib.auth.decorators import permission_required
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication.jwt_authentication import JWTAuthentication
from courses.api.serializer import AuthorSerializer
from .models import Author


# Create your views here.
class CreateAuthorAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = AuthorSerializer(data=user)
        serializer.is_valid(raise_exception=True)

        jwt_authentication = JWTAuthentication("Author", serializer.validated_data)
        jwt_token = jwt_authentication.create_jwt()

        serializer.save()

        return Response({'message': 'Success', 'username': request.data.get('email'),
                         'token': jwt_token},
                        status=status.HTTP_201_CREATED)


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
    permission_classes = ('get_all_authors', )

    def post(self, request):
        jwt_request = request.data
        author = Author.objects.filter(email=jwt_request.get("data"))
        jwt_authentication_request = JWTAuthentication("Author", author)
        response, payload = jwt_authentication_request.authenticate(request=request)

        return Response({'message': 'Authenticated', 'body': response}, status=status.HTTP_202_ACCEPTED)


class ObtainAuthorsView(APIView):
    serializer_class = AuthorSerializer

    def get(self, request):
        jwt_authenticator = JWTAuthentication('Author', request.data)
        jwt_response, payload = jwt_authenticator.authenticate(request)

        if jwt_response is None:
            return Response({'message': 'Not Authenticated'}, status=status.HTTP_204_NO_CONTENT)

        serializer = self.serializer_class(Author.objects.all(), many=True)
        return Response({'data': serializer.data, 'payload': payload}, status=status.HTTP_200_OK)


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
