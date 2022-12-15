from django.core.mail import send_mail
from core.models import PortfolioMessage
from django.utils import timezone
import re


def validate_limit_message_in_a_minutes(ip_address: str):
    """validate when user send too much message in a minutes
    maximum is 3 message in a minutes"""
    try:
        PortfolioMessage.objects.filter(ip_address=ip_address).filter(
            created_at__gte=timezone.now() - timezone.timedelta(minutes=1)
        )[2]
        return False
    except IndexError:
        return True


def validate_ip_address(ip_address: str):
    """validate IP address is the right format"""
    pattern = re.compile(r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.)"
                         r"{3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])")
    return re.fullmatch(pattern, ip_address)


def send_notify_email(message: PortfolioMessage):
    message_template = f'from {message.name_or_email},\n' \
                       f'{message.message},\n' \
                       f'{message.created_at},\n' \
                       f'{message.ip_address}'
    send_mail(
        'Portfolio Message',
        message_template,
        'maitocode@gmail.com',
        ['qitpydev@gmail.com'],
        fail_silently=False,
    )
