from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt


def admin_required():

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if claims["role"] != "admin":
                return {"msg": "Acesso negado"}, 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator
