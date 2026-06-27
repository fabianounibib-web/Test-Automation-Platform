import os
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from app.database.models import Roteiro, CasoTeste, Cliente, User
from app.helpers import response_success, response_error

roteiros_bp = Blueprint('roteiros', __name__)


def serialize_roteiro(roteiro):
    """Serialize roteiro to dict."""
    return {
        'id': roteiro.id,
        'cliente_id': roteiro.cliente_id,
        'arquivo': roteiro.arquivo,
        'status': roteiro.status,
        'created_at': roteiro.created_at.isoformat() if hasattr(roteiro, 'created_at') else None,
    }


@roteiros_bp.route('', methods=['GET'])
@jwt_required()
def get_roteiros(current_user_id):
    """List all roteiros (paginated, with filters)."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    cliente_id = request.args.get('cliente_id', type=int)
    status = request.args.get('status', type=str)
    
    query = Roteiro.query
    
    if cliente_id:
        query = query.filter_by(cliente_id=cliente_id)
    
    if status:
        query = query.filter_by(status=status)
    
    query = query.order_by(Roteiro.id.desc())
    paginated = query.paginate(page=max(1, page), per_page=min(100, max(1, per_page)), error_out=False)
    
    return response_success({
        'items': [serialize_roteiro(r) for r in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'per_page': per_page,
    })


@roteiros_bp.route('/<int:roteiro_id>', methods=['GET'])
@jwt_required()
def get_roteiro(current_user_id, roteiro_id):
    """Get a specific roteiro by ID."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    roteiro = Roteiro.query.get(roteiro_id)
    if not roteiro:
        return response_error('Roteiro não encontrado', 404)

    return response_success(serialize_roteiro(roteiro))


@roteiros_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_roteiro(current_user_id):
    """Upload a roteiro file (XLS, CSV, JSON)."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    if 'file' not in request.files:
        return response_error('Arquivo não enviado', 400)

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return response_error('Arquivo vazio', 400)

    cliente_id = request.form.get('cliente_id', type=int)
    if not cliente_id:
        return response_error('Cliente ID é obrigatório', 400)

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return response_error('Cliente não encontrado', 404)

    # Validate file extension
    allowed_extensions = {'xls', 'xlsx', 'csv', 'json'}
    if '.' not in uploaded_file.filename or \
       uploaded_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return response_error('Formato de arquivo não permitido. Use: XLS, XLSX, CSV, JSON', 400)

    filename = secure_filename(uploaded_file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    destination = os.path.join(upload_folder, filename)
    uploaded_file.save(destination)

    roteiro = Roteiro(
        cliente_id=cliente_id,
        arquivo=filename,
        status='uploaded'
    )
    db.session.add(roteiro)
    db.session.commit()

    return response_success(serialize_roteiro(roteiro), 'Roteiro importado com sucesso', 201)


@roteiros_bp.route('/<int:roteiro_id>', methods=['DELETE'])
@jwt_required()
def delete_roteiro(current_user_id, roteiro_id):
    """Delete a roteiro."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    roteiro = Roteiro.query.get(roteiro_id)
    if not roteiro:
        return response_error('Roteiro não encontrado', 404)

    # Delete associated file
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, roteiro.arquivo)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        current_app.logger.error(f'Error deleting file: {e}')

    db.session.delete(roteiro)
    db.session.commit()

    return response_success(None, 'Roteiro removido com sucesso')
