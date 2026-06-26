from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # register blueprints (import locally to avoid circular imports)
    try:
        from app.auth.routes import auth_bp
        from app.clientes.routes import clientes_bp
        from app.roteiros.routes import roteiros_bp
        from app.testes.routes import testes_bp
        from app.execucoes.routes import execucoes_bp
        from app.evidencias.routes import evidencias_bp
        from app.logs.routes import logs_bp
        from app.core.routes import core_bp

        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
        app.register_blueprint(roteiros_bp, url_prefix='/api/roteiros')
        app.register_blueprint(testes_bp, url_prefix='/api/casos')
        app.register_blueprint(execucoes_bp, url_prefix='/api/execucoes')
        app.register_blueprint(evidencias_bp, url_prefix='/api/evidencias')
        app.register_blueprint(logs_bp, url_prefix='/api/logs')
        app.register_blueprint(core_bp, url_prefix='/api')
    except Exception:
        pass

    return app
