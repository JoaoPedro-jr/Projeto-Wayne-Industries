from flask import Blueprint, render_template, redirect, url_for, flash , request
from flask_login import login_required, current_user, logout_user
from app import db
from app.models import nivel_model
recursos_bp = Blueprint('recursos', __name__)


@recursos_bp.route('/recursos')
@login_required
def recursos():
    from app.models.equipamentos_model import EquipamentoModel
    from app.models.dispositivos_model import DispositivoModel
    from app.models.veiculos_model import VeiculoModel

    equipamentos = EquipamentoModel.query.all()
    dispositivos = DispositivoModel.query.all()
    veiculos = VeiculoModel.query.all()

    return render_template(
        'pages/recursos.html',
        equipamentos=equipamentos,
        dispositivos=dispositivos,
        veiculos=veiculos
    )



@recursos_bp.route('/recursos/criar_recurso', methods=['GET', 'POST'])
@login_required
def criar_recursos():
    if not current_user.is_admin():
        flash('Acesso negado!', 'danger')
        return redirect(url_for('recursos.recursos'))

    from app.models.equipamentos_model import EquipamentoModel
    from app.models.dispositivos_model import DispositivoModel
    from app.models.veiculos_model import VeiculoModel

    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        tipo = request.form.get('tipo')
        ativo = bool(request.form.get('ativo'))
        if not nome or not descricao or not tipo:
            flash('Preencha todos os campos!', 'warning')
        else:
            if tipo == 'equipamento':
                novo = EquipamentoModel(nome=nome, descricao=descricao, ativo=ativo)
            elif tipo == 'veiculo':
                novo = VeiculoModel(nome=nome, descricao=descricao, ativo=ativo)
            elif tipo == 'dispositivo':
                novo = DispositivoModel(nome=nome, descricao=descricao, ativo=ativo)
            else:
                flash('Tipo de recurso inválido!', 'danger')
                return redirect(url_for('recursos.recursos'))
            db.session.add(novo)
            db.session.commit()
            flash(f'{tipo.capitalize()} adicionado com sucesso!', 'success')
        return redirect(url_for('recursos.recursos'))

    # GET: apenas renderiza a tela com os dados atuais
    equipamentos = EquipamentoModel.query.all()
    dispositivos = DispositivoModel.query.all()
    veiculos = VeiculoModel.query.all()
    return render_template('pages/recursos.html', equipamentos=equipamentos, dispositivos=dispositivos, veiculos=veiculos)

# Exemplo de rota para remover recurso (pode ser adaptada para editar também)
@recursos_bp.route('/recursos/remover/<tipo>/<int:id>', methods=['POST'])
@login_required
def remover_recurso(tipo, id):
    if not current_user.is_admin():
        flash('Acesso negado!', 'danger')
        return redirect(url_for('recursos.recursos'))
    model = None
    if tipo == 'equipamento':
        from app.models.equipamentos_model import EquipamentoModel
        model = EquipamentoModel
    elif tipo == 'veiculo':
        from app.models.veiculos_model import VeiculoModel
        model = VeiculoModel
    elif tipo == 'dispositivo':
        from app.models.dispositivos_model import DispositivoModel
        model = DispositivoModel
    else:
        flash('Tipo de recurso inválido!', 'danger')
        return redirect(url_for('recursos.recursos'))
    recurso = model.query.get_or_404(id)
    db.session.delete(recurso)
    db.session.commit()
    flash(f'{tipo.capitalize()} removido com sucesso!', 'success')
    return redirect(url_for('recursos.recursos'))

@recursos_bp.route('/recursos/editar_equipamento/<int:id>', methods=['POST'])
@login_required
def editar_equipamento(id):
    if not current_user.is_admin():
        flash('Acesso negado!', 'danger')
        return redirect(url_for('recursos.recursos'))
    from app.models.equipamentos_model import EquipamentoModel
    equipamento = EquipamentoModel.query.get_or_404(id)
    equipamento.nome = request.form.get('nome')
    equipamento.descricao = request.form.get('descricao')
    equipamento.ativo = bool(request.form.get('ativo'))
    db.session.commit()
    flash('Equipamento atualizado com sucesso!', 'success')
    return redirect(url_for('recursos.recursos'))

