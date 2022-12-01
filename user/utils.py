from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re


def is_email_valid(value):
    # Validate a single email
    message_invalid = "Enter a valid email address"

    if not value:
        return False, message_invalid

    # Check the regex, using the validate_email from django
    try:
        validate_email(value)
    except ValidationError:
        return False, message_invalid

    return True, ""


def is_username_valid(value):
    # Validate a single username
    message_invalid = "Enter a valid username"

    if not value:
        return False, message_invalid

    # Check the regex against username using instagram username regex rules
    matched = re.match("^[\w](?!.*?\.{2})[\w.]{1,28}[\w]$", value)
    if not bool(matched):
        return False, message_invalid

    return True, ""
