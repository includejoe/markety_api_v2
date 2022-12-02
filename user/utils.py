from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
import json
from rest_framework.renderers import JSONRenderer


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


# junk code: to be removed
# Custom JSON Renderer
class UserJSONRenderer(JSONRenderer):
    # Custom method
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get("errors", None)
        token = data.get("token", None)

        if errors is not None:
            return super(UserJSONRenderer, self).render(data)

        if token is not None and isinstance(token, bytes):
            data["token"] = token.decode("utf-8")

        return json.dumps({"user": data})
