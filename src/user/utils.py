from google.auth.transport import requests
from google.oauth2 import id_token
from core.exceptions.exceptions import RegisterWithGoogleTokenInvalid
import os


def login_with_google_and_get_info(google_credential: str):
    user_name = None
    user_email = None
    try:
        CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
        user_info = id_token.verify_oauth2_token(
                google_credential, requests.Request(), CLIENT_ID
            )
        user_email = user_info['email']
        user_name = user_info['name'] | "No name"
    except ValueError:
        raise RegisterWithGoogleTokenInvalid()

    return user_email, user_name
