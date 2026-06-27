from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.database.models import User
from app.helpers import response_success, response_error

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login with email and password."""
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    senha = data.get('senha') or ''

    if not email or not senha:
        return response_error('Email e senha são obrigatórios', 400)

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.senha, senha):
        return response_error('Credenciais inválidas', 401)

    token = create_access_token(identity=user.id)
    return response_success({
        'access_token': token,
        'user': {
            'id': user.id,
            'nome': user.nome,
            'email': user.email,
            'perfil': user.perfil
        }
    }, 'Login realizado com sucesso', 200)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json() or {}
    nome = (data.get('nome') or '').strip()
    email = (data.get('email') or '').strip().lower()
    senha = data.get('senha') or ''

    if not nome or not email or not senha:
        return response_error('Nome, email e senha são obrigatórios', 400)

    if User.query.filter_by(email=email).first():
        return response_error('Usuário já existe', 409)

    user = User(
        nome=nome,
        email=email,
        senha=generate_password_hash(senha),
        perfil=data.get('perfil', 'analista')
    )
    db.session.add(user)
    db.session.commit()

    return response_success({
        'id': user.id,
        'nome': user.nome,
        'email': user.email,
        'perfil': user.perfil
    }, 'Usuário criado com sucesso', 201)


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    return response_success({
        'id': user.id,
        'nome': user.nome,
        'email': user.email,
        'perfil': user.perfil
    })


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_token():
    """Refresh access token."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    token = create_access_token(identity=user.id)
    return response_success({
        'access_token': token,
        'user': {
            'id': user.id,
            'nome': user.nome,
            'email': user.email,
            'perfil': user.perfil
        }
    }, 'Token atualizado com sucesso')
