from rest_framework import status
from rest_framework.exceptions import APIException


class TypeErrorException(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'field_error'


class FieldErrorException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'field_error'


class LookUpError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'lookup_error'


class AttributeErrorException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'attribute_error'


class SaveUserError(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'save_user_error'


class IncorrectEmailError(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'email_error'
