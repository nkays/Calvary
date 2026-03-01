from django.core.exceptions import ValidationError


def validate_blocked_email(value):
    """Validator for blocking specific email domains."""
    blocked_domains = ['hotmail.com', 'test.com']
    domain = value.split('@')[-1]
    if domain in blocked_domains:
        raise ValidationError(f"Email addresses from {domain} are not allowed.")