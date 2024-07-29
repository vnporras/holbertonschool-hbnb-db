from typing import Literal
from email_validator import validate_email as _validate, EmailNotValidError


def validate_email(
    email: str, validate_dns: bool = False
) -> str | Literal[False]:
    """Validates an email address and returns the normalized version if valid."""

    try:
        emailinfo = _validate(email, check_deliverability=validate_dns)
    except EmailNotValidError:
        return False

    return emailinfo.normalized
