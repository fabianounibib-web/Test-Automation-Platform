from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.database.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    senha = data.get('senha') or ''

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.senha, senha):
        return jsonify({'error': 'credenciais inválidas'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token, 'user': {'id': user.id, 'nome': user.nome, 'email': user.email, 'perfil': user.perfil}}), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    nome = (data.get('nome') or '').strip()
    email = (data.get('email') or '').strip().lower()
    senha = data.get('senha') or ''

    if not nome or not email or not senha:
        return jsonify({'error': 'nome, email e senha são obrigatórios'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'usuário já existe'}), 409

    user = User(nome=nome, email=email, senha=generate_password_hash(senha), perfil=data.get('perfil') or 'analista')
    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': 'usuário criado com sucesso', 'user': {'id': user.id, 'nome': user.nome, 'email': user.email, 'perfil': user.perfil}}), 201
