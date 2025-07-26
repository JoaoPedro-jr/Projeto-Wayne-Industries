from app import db
from flask_login import UserMixin
from app import bcrypt
from datetime import datetime

class UsuarioModel(UserMixin , db.Model):
    __tablename__ = 'tb_usuarios'
    usuario_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(128), nullable=False)
    from .nivel_model import NivelModel
    # Relacionamento com o modelo NivelModel
    nivel_id = db.Column(db.Integer, db.ForeignKey('tb_niveis.nivel_id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ultimo_acesso = db.Column(db.DateTime)
    tentativas_login = db.Column(db.Integer, default=0)
    nivel = db.relationship('NivelModel', backref='usuarios')

    def get_id(self):
        return str(self.usuario_id)

    def set_senha(self, senha):
        self.senha = bcrypt.generate_password_hash(senha).decode('utf-8')
    

    def check_senha(self, senha):
        return bcrypt.check_password_hash(self.senha, senha)

    def is_admin(self):
        return self.nivel.nome == 'Administrador'