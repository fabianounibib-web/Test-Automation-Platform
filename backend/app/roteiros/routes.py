import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db
from app.database.models import Roteiro, CasoTeste

roteiros_bp = Blueprint('roteiros', __name__)


@roteiros_bp.route('', methods=['GET'])
def get_roteiros():
    roteiros = Roteiro.query.order_by(Roteiro.id.desc()).all()
    return jsonify([
        {
            'id': roteiro.id,
            'cliente_id': roteiro.cliente_id,
            'arquivo': roteiro.arquivo,
            'status': roteiro.status
        }
        for roteiro in roteiros
    ]), 200


@roteiros_bp.route('/upload', methods=['POST'])
def upload_roteiro():
    if 'file' not in request.files:
        return jsonify({'error': 'arquivo não enviado'}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({'error': 'arquivo vazio'}), 400

    filename = secure_filename(uploaded_file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    destination = os.path.join(upload_folder, filename)
    uploaded_file.save(destination)

    roteiro = Roteiro(arquivo=filename, status='uploaded')
    db.session.add(roteiro)
    db.session.commit()

    caso = CasoTeste(
        roteiro_id=roteiro.id,
        nome=f'Caso do roteiro {filename}',
        objetivo='Caso gerado automaticamente a partir do roteiro importado.',
        dados={'arquivo': filename},
        resultado_esperado='Execução concluída sem erros.',
        status='created'
    )
    db.session.add(caso)
    db.session.commit()

    return jsonify({
        'id': roteiro.id,
        'arquivo': roteiro.arquivo,
        'status': roteiro.status,
        'caso_id': caso.id
    }), 201
