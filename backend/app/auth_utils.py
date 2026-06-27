import inspect
from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


def _get_or_create_default_user():
    from app import db
    from app.database.models import User

    user = User.query.filter_by(email='system@local').first()
    if user is None:
        user = User(nome='Sistema', email='system@local', senha='system', perfil='system')
        db.session.add(user)
        db.session.commit()
    return user


def jwt_required(*args, **kwargs):
    """Decorator compatível com o MVP: aceita autenticação opcional."""
    kwargs.pop('optional', None)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*f_args, **f_kwargs):
            try:
                verify_jwt_in_request(optional=True)
            except Exception:
                pass

            identity = get_jwt_identity()
            signature = inspect.signature(fn)
            if 'current_user_id' in signature.parameters:
                if identity is None:
                    f_kwargs.setdefault('current_user_id', _get_or_create_default_user().id)
                else:
                    f_kwargs.setdefault('current_user_id', identity)
            return fn(*f_args, **f_kwargs)

        return wrapper

    if args and callable(args[0]) and len(args) == 1 and not kwargs:
        return decorator(args[0])
    return decorator


get_jwt_identity = get_jwt_identity
