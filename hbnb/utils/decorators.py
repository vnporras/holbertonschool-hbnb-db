from functools import wraps
from typing import Any, Callable
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def admin_required():
    def wrapper(fn: Callable[..., tuple[dict[str, Any], int]]):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception:
                return {"error": "Missing Authorization Header"}, 401
            claims = get_jwt()
            if claims.get("is_admin") == True:
                return fn(*args, **kwargs)
            else:
                return {"error": "Forbidden"}, 403

        return decorator

    return wrapper
