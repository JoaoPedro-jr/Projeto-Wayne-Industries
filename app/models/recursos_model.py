from app import db
from flask_login import UserMixin
from app import bcrypt
from datetime import datetime

class RecursosModel(UserMixin, db.Model):
    __tablename__ = 'tb_recursos'
    
    recurso_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

