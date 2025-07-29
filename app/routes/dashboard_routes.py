from flask import Blueprint, render_template
from flask_login import login_required
from app.models.usuario_model import UsuarioModel
from app.models.nivel_model import NivelModel
dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard_view():
    usuarios_ativos = UsuarioModel.query.filter_by(ativo=True).count()
    niveis_count = NivelModel.query.count()
    return render_template('pages/dashboard.html', usuarios_ativos=usuarios_ativos, niveis_count=niveis_count)


@dashboard_bp.route('/dashboard/usuarios')
@login_required
def dashboard_usuarios():
    usuarios = UsuarioModel.query.all()
    return render_template('pages/dashboard_usuarios.html', usuarios=usuarios)
@dashboard_bp.route('/dashboard/niveis')
@login_required
def dashboard_niveis():
    niveis = NivelModel.query.all()
    return render_template('pages/dashboard_niveis.html', niveis=niveis)
