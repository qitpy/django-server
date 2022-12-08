from rest_framework.exceptions import APIException


class RegisterWithGoogleTokenInvalid(APIException):
    status_code = 400
    default_detail = 'your token provide is not valid or expired!'
    default_code = 'token_invalid'
