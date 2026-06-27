from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    perfil = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    responsavel = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Sistema(db.Model):
    __tablename__ = 'sistemas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200))
    tipo = db.Column(db.String(50))
    endpoint = db.Column(db.String(500))
    credenciais = db.Column(db.JSON)


class Conector(db.Model):
    __tablename__ = 'conectores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    url_base = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.String(50), default='web')  # web, sap, desktop, api, legacy
    ambiente = db.Column(db.String(80), default='desenvolvimento')  # desenvolvimento, homologacao, producao_assistida
    status = db.Column(db.String(50), default='draft')  # draft, ativo, inativo
    versao = db.Column(db.String(50), default='1.0.0')
    credenciais_ref = db.Column(db.JSON, default=dict)
    steps = db.Column(db.JSON, default=list)  # Recorded automation steps as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Roteiro(db.Model):
    __tablename__ = 'roteiros'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    arquivo = db.Column(db.String(500))
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CasoTeste(db.Model):
    __tablename__ = 'casos_teste'
    id = db.Column(db.Integer, primary_key=True)
    roteiro_id = db.Column(db.Integer, db.ForeignKey('roteiros.id'))
    nome = db.Column(db.String(300))
    objetivo = db.Column(db.Text)
    dados = db.Column(db.JSON)  # Test data/parameters
    resultado_esperado = db.Column(db.Text)
    status = db.Column(db.String(50), default='criado')  # criado, validado, aguardando_dados, pronto, em_execucao, sucesso, erro, inconcluso, cancelado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Robo(db.Model):
    __tablename__ = 'robos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(300), nullable=False)
    descricao = db.Column(db.Text)
    tipo = db.Column(db.String(100), default='python')
    script = db.Column(db.Text)
    status = db.Column(db.String(50), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Execucao(db.Model):
    __tablename__ = 'execucoes'
    id = db.Column(db.Integer, primary_key=True)
    caso_teste_id = db.Column(db.Integer, db.ForeignKey('casos_teste.id'))
    robo_id = db.Column(db.Integer, db.ForeignKey('robos.id'))
    inicio = db.Column(db.DateTime)
    fim = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    tempo = db.Column(db.Float)
    rpa_id = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    execucao_id = db.Column(db.Integer, db.ForeignKey('execucoes.id'))
    nivel = db.Column(db.String(20))
    mensagem = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Evidencia(db.Model):
    __tablename__ = 'evidencias'
    id = db.Column(db.Integer, primary_key=True)
    execucao_id = db.Column(db.Integer, db.ForeignKey('execucoes.id'))
    arquivo = db.Column(db.String(500))
    tipo = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Configuracao(db.Model):
    __tablename__ = 'configuracoes'
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(200))
    valor = db.Column(db.String(500))
