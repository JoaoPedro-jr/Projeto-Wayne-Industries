from app import db
from datetime import datetime

class AtividadeLogModel(db.Model):
    __tablename__ = 'atividades_logs'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=True)  # pode ser null para ações do sistema
    acao = db.Column(db.String(100), nullable=False)
    detalhes = db.Column(db.Text)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
