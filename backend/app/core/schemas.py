from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    senha = fields.Str(load_only=True, required=True)
    perfil = fields.Str(validate=validate.Length(max=50))
    created_at = fields.DateTime(dump_only=True)


class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email()
    responsavel = fields.Str(validate=validate.Length(max=100))
    created_at = fields.DateTime(dump_only=True)


class SistemaSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    tipo = fields.Str()
    endpoint = fields.Str()
    credenciais = fields.Dict()
    created_at = fields.DateTime(dump_only=True)


class RoteiroSchema(Schema):
    id = fields.Int(dump_only=True)
    cliente_id = fields.Int(required=True)
    arquivo = fields.Str(dump_only=True)
    status = fields.Str()
    created_at = fields.DateTime(dump_only=True)


class CasoTesteSchema(Schema):
    id = fields.Int(dump_only=True)
    roteiro_id = fields.Int(required=True)
    nome = fields.Str(required=True)
    objetivo = fields.Str()
    dados = fields.Dict()
    resultado_esperado = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime(dump_only=True)


class RoboSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    descricao = fields.Str()
    tipo = fields.Str()
    script = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime(dump_only=True)


class ExecucaoSchema(Schema):
    id = fields.Int(dump_only=True)
    caso_teste_id = fields.Int(required=False)
    robo_id = fields.Int(required=False)
    inicio = fields.DateTime()
    fim = fields.DateTime()
    status = fields.Str()
    tempo = fields.Float()
    rpa_id = fields.Str()
    created_at = fields.DateTime(dump_only=True)


class LogSchema(Schema):
    id = fields.Int(dump_only=True)
    execucao_id = fields.Int(required=True)
    nivel = fields.Str()
    mensagem = fields.Str()
    timestamp = fields.DateTime(dump_only=True)


class EvidenciaSchema(Schema):
    id = fields.Int(dump_only=True)
    execucao_id = fields.Int(required=True)
    arquivo = fields.Str()
    tipo = fields.Str()
    created_at = fields.DateTime(dump_only=True)
