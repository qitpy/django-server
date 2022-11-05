from django.conf import settings
import datetime

def is_expired_verify_email_code(self, verify_start_at):
    '''return True if it's expired for verify, & against'''
    delta_time = datetime.datetime.now() - verify_start_at
    seconds = delta_time.seconds
    return seconds > 60 * settings.AUTH_VERIFY_EMAIL_EXPIRED_MINUTES

