"""
database.py - Modelos e configuração do banco de dados
Integração SQLite/PostgreSQL com SQLAlchemy
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # admin, tecnico, usuario
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relações
    chamados = db.relationship(
        'Chamado',
        foreign_keys='Chamado.usuario_id',
        backref='usuario',
        lazy=True
    )
    chamados_atribuidos = db.relationship(
        'Chamado',
        foreign_keys='Chamado.tecnico_id',
        backref='tecnico',
        lazy=True
    )
    logs_auditoria = db.relationship('LogAuditoria', backref='usuario', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo': self.tipo,
            'criado_em': self.criado_em.isoformat()
        }


class Chamado(db.Model):
    __tablename__ = 'chamados'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nome_solicitante = db.Column(db.String(120), nullable=False)
    setor = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Aberto')  # Aberto, Em andamento, Fechado
    tecnico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fechado_em = db.Column(db.DateTime, nullable=True)
    
    # Relações
    logs_auditoria = db.relationship('LogAuditoria', backref='chamado', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'nome_solicitante': self.nome_solicitante,
            'setor': self.setor,
            'descricao': self.descricao,
            'status': self.status,
            'tecnico_id': self.tecnico_id,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat(),
            'fechado_em': self.fechado_em.isoformat() if self.fechado_em else None
        }


class LogAuditoria(db.Model):
    __tablename__ = 'log_auditoria'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    chamado_id = db.Column(db.Integer, db.ForeignKey('chamados.id'), nullable=True)
    acao = db.Column(db.String(100), nullable=False)  # criar, atualizar, deletar, login, etc
    tabela_afetada = db.Column(db.String(50), nullable=False)  # usuarios, chamados, login
    dados_anteriores = db.Column(db.JSON, nullable=True)  # JSON com dados antes
    dados_novos = db.Column(db.JSON, nullable=True)      # JSON com dados depois
    endereco_ip = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'chamado_id': self.chamado_id,
            'acao': self.acao,
            'tabela_afetada': self.tabela_afetada,
            'dados_anteriores': self.dados_anteriores,
            'dados_novos': self.dados_novos,
            'endereco_ip': self.endereco_ip,
            'timestamp': self.timestamp.isoformat()
        }


class Backup(db.Model):
    __tablename__ = 'backups'
    id = db.Column(db.Integer, primary_key=True)
    arquivo = db.Column(db.String(255), nullable=False)
    caminho = db.Column(db.String(500), nullable=False)
    tamanho_bytes = db.Column(db.Integer)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    hash_md5 = db.Column(db.String(32), nullable=True)  # Para verificar integridade

    def to_dict(self):
        return {
            'id': self.id,
            'arquivo': self.arquivo,
            'caminho': self.caminho,
            'tamanho_mb': round(self.tamanho_bytes / (1024*1024), 2) if self.tamanho_bytes else 0,
            'criado_em': self.criado_em.isoformat(),
            'hash_md5': self.hash_md5
        }
