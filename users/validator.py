# from email import message
import re

from django.core.exceptions import ValidationError

def validate_email(email):
    EMAIL_REGEX = re.match('^[a-zA-z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+$', email)
    if not EMAIL_REGEX:
        raise ValidationError(message="INVALID_EMAIL")

def validate_password(password):
    PASSWORD_REGEX = re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$', password)
    if not PASSWORD_REGEX:
        raise ValidationError(message="INVALID_PASSWORD")