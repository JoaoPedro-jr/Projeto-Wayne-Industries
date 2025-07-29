from flask import Blueprint, render_template, redirect, url_for, flash , request
from flask_login import login_required, current_user, logout_user
from app import db
from app.models import nivel_model
niveis_bp = Blueprint('niveis', __name__)





@niveis_bp.route('/niveis')
@login_required
def listar_niveis():
    from app.models.nivel_model import NivelModel
    niveis = NivelModel.query.all()
    return render_template('pages/niveis.html', niveis=niveis)

@niveis_bp.route('/niveis/editar/<int:id>', methods=['GET'])
@login_required
def editar_nivel(id):
    if not current_user.is_admin():
        flash('Acesso negado!')
        return redirect(url_for('dashboard_bp.dashboard_view'))
    from app.models.nivel_model import NivelModel
    nivel = NivelModel.query.get_or_404(id)
    niveis = NivelModel.query.all()

    if request.method == 'POST':
        nome_nivel = request.form.get('nome')
        descricao = request.form.get('descricao')
        if not nome_nivel or not descricao:
            flash('Preencha todos os campos!', 'warning')
            return render_template('pages/niveis.html', nivel=nivel, niveis=niveis)
        
        if NivelModel.query.filter(NivelModel.nome == nome_nivel, NivelModel.nivel_id != id).first():
            flash('Esse nome já existe!', 'error')
            return render_template('pages/niveis.html', nivel=nivel, niveis=niveis)
        
        nivel.nome = nome_nivel
        nivel.descricao = descricao

        db.session.commit()
        flash('Nível atualizado com sucesso!', 'success')
        return redirect(url_for('niveis.listar_niveis'))

    return render_template('pages/niveis.html', nivel=nivel, niveis=niveis)



@niveis_bp.route('/niveis/delete/<int:id>', methods=['POST'])
@login_required
def excluir_nivel(id):
    if not current_user.is_admin():
        flash('Acesso negado!')
        return redirect(url_for('dashboard_bp.dashboard_view'))

    from app.models.nivel_model import NivelModel
    nivel = NivelModel.query.get_or_404(id)
    if nivel.usuario and len(nivel.usuarios) > 0:
        flash('Não é possível excluir: existem usuários vinculados a este nível.', 'warning')
        return redirect(url_for('niveis.listar_niveis'))
    db.session.delete(nivel)
    db.session.commit()
    flash('Nível excluído com sucesso!', 'success')
    return redirect(url_for('niveis.listar_niveis'))



@niveis_bp.route('/niveis/adicionar', methods=['POST'])
@login_required
def adicionar_nivel():
    if not current_user.is_admin():
        flash('Acesso negado!')
        return redirect(url_for('dashboard_bp.dashboard_view'))
    from app.models.nivel_model import NivelModel
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    if not nome or not descricao:
        flash('Preencha todos os campos!', 'warning')
        return redirect(url_for('niveis.listar_niveis'))
    if NivelModel.query.filter_by(nome=nome).first():
        flash('Esse nome já existe!', 'error')
        return redirect(url_for('niveis.listar_niveis'))
    novo_nivel = NivelModel(nome=nome, descricao=descricao)
    db.session.add(novo_nivel)
    db.session.commit()
    flash('Nível criado com sucesso!', 'success')
    return redirect(url_for('niveis.listar_niveis'))