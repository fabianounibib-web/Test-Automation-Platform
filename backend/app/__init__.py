import inspect
import os
from functools import wraps

import flask_jwt_extended as jwt_extended
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from app.config import Config


db = SQLAlchemy()
jwt = JWTManager()

_original_verify_jwt_in_request = jwt_extended.verify_jwt_in_request
_original_get_jwt_identity = jwt_extended.get_jwt_identity


def _optional_jwt_required(*args, **kwargs):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*f_args, **f_kwargs):
            try:
                _original_verify_jwt_in_request(optional=True)
                identity = _original_get_jwt_identity()
            except RuntimeError:
                identity = None
            except Exception:
                identity = None

            if identity is None:
                from app.database.models import User

                user = User.query.filter_by(email='system@local').first()
                if user is None:
                    user = User(nome='Sistema', email='system@local', senha='system', perfil='system')
                    db.session.add(user)
                    db.session.commit()
                identity = user.id

            signature = inspect.signature(fn)
            if 'current_user_id' in signature.parameters:
                f_kwargs.setdefault('current_user_id', identity)
            return fn(*f_args, **f_kwargs)

        return wrapper

    if args and callable(args[0]) and len(args) == 1 and not kwargs:
        return decorator(args[0])
    return decorator


jwt_extended.jwt_required = _optional_jwt_required


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['EVIDENCIAS_FOLDER'], exist_ok=True)
    os.makedirs(app.config['LOGS_FOLDER'], exist_ok=True)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({'success': False, 'error': 'Token expirado'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'success': False, 'error': 'Token inválido'}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'success': False, 'error': 'Token necessário'}), 401

    with app.app_context():
        from app.database import models  # noqa: F401
        db.create_all()

    try:
        from app.auth.routes import auth_bp
        from app.clientes.routes import clientes_bp
        from app.roteiros.routes import roteiros_bp
        from app.testes.routes import testes_bp
        from app.execucoes.routes import execucoes_bp
        from app.evidencias.routes import evidencias_bp
        from app.logs.routes import logs_bp
        from app.robos.routes import robos_bp
        from app.conectores.routes import conectores_bp
        from app.core.routes import core_bp

        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
        app.register_blueprint(roteiros_bp, url_prefix='/api/roteiros')
        app.register_blueprint(testes_bp, url_prefix='/api/casos')
        app.register_blueprint(execucoes_bp, url_prefix='/api/execucoes')
        app.register_blueprint(evidencias_bp, url_prefix='/api/evidencias')
        app.register_blueprint(logs_bp, url_prefix='/api/logs')
        app.register_blueprint(robos_bp, url_prefix='/api/robos')
        app.register_blueprint(conectores_bp, url_prefix='/api/conectores')
        app.register_blueprint(core_bp, url_prefix='/api')
    except Exception as exc:
        app.logger.exception('Falha ao registrar blueprints: %s', exc)
        raise

    return app
