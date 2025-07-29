from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from app import db
from app.models.atividades_logs_model import AtividadeLogModel
logs_bp = Blueprint('logs', __name__)


@logs_bp.route('/logs')
@login_required
def listar_logs():
    logs = AtividadeLogModel.query.order_by(AtividadeLogModel.data_hora.desc()).all()
    return render_template('pages/logs.html', logs=logs)


@logs_bp.route('/logs/usuarios/<int:usuario_id>')
@login_required
def logs_usuario(usuario_id):
    logs = AtividadeLogModel.query.filter_by(usuario_id=usuario_id).order_by(AtividadeLogModel.data_hora.desc()).all()
    return render_template('pages/logs.html', logs=logs)