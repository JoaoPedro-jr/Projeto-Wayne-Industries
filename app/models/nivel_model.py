from app import db

class NivelModel(db.Model):
    __tablename__ = 'tb_niveis'

    nivel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    descricao = db.Column(db.String(255), nullable=True)