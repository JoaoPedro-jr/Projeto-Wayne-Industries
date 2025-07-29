from flask import Blueprint, redirect, url_for, request, flash, render_template
from flask_login import current_user, login_required
from app.models.usuario_model import UsuarioModel
from app import db

# aqui to criando o blueprint de usuários
usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['GET'])
@login_required
def listar_usuarios():
    # aqui eu busco todos os usuários do banco de dados
    from app.models.nivel_model import NivelModel
    usuarios = UsuarioModel.query.all()
    niveis = NivelModel.query.all()
    return render_template('usuarios/usuarios.html', usuarios=usuarios, niveis=niveis)


@usuarios_bp.route('/usuarios/api', methods=['GET'])
@login_required
def api_usuarios():
    # aqui eu crio uma rota para a API que retorna todos os usuários em formato JSON
    usuarios = UsuarioModel.query.all()
    usuarios_json = [
        {
            'usuario_id': usuario.usuario_id,
            'nome': usuario.nome,
            'email': usuario.email,
            'nivel': usuario.nivel.nome if usuario.nivel else 'Nenhum'
        } for usuario in usuarios
    ]

    return {"usuarios": usuarios_json}

@usuarios_bp.route("/api/usuarios/", methods=["GET", "POST"])
@login_required
def criar_usuario():
    if not current_user.is_admin():
        flash('Acesso negado!')
        return redirect(url_for('dashboard_bp.dashboard_view'))
    from app.models.nivel_model import NivelModel
    usuarios = UsuarioModel.query.all()
    niveis = NivelModel.query.all()
    if request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        nivel = request.form.get('nivel')
        print(f"[DEBUG] nome={nome}, email={email}, nivel={nivel}")
        try:
            nivel = int(nivel)
        except (TypeError, ValueError):
            nivel = None

        # Buscar o objeto do nível pelo id e mostrar o nome
        nivel_obj = NivelModel.query.get(nivel) if nivel is not None else None
        if nivel_obj:
            print(f"[DEBUG] Nível selecionado: id={nivel}, nome={nivel_obj.nome}")
        else:
            print(f"[DEBUG] Nível id={nivel} não encontrado")

        senha = 'default123'  # Senha padrão, deve ser alterada pelo usuário

        if not nome or not email or nivel is None:
            flash('Preencha todos os campos!', 'warning')
            return render_template('usuarios/usuarios.html', usuarios=usuarios, niveis=niveis)
        
        if UsuarioModel.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'error')
            return render_template('usuarios/usuarios.html', usuarios=usuarios, niveis=niveis)

        novo_usuario = UsuarioModel(nome=nome, 
                                    email=email, 
                                    nivel_id=nivel)
        novo_usuario.set_senha(senha)  # Define a senha usando o método set_senha
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))
    return render_template('usuarios/usuarios.html', usuarios=usuarios, niveis=niveis)



@usuarios_bp.route("/api/usuarios/<int:id>", methods=["POST"])
@login_required
def excluir_usuario(id):
    if not current_user.is_admin():
        flash('Acesso negado!')
        return redirect(url_for('dashboard_bp.dashboard_view'))
    usuario = UsuarioModel.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for("usuarios.listar_usuarios"))

@usuarios_bp.route('/api/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    if not current_user.is_admin():
        flash('Acesso negado!')
        return redirect(url_for('dashboard_bp.dashboard_view'))
    from app.models.nivel_model import NivelModel
    usuario = UsuarioModel.query.get_or_404(id)
    usuarios = UsuarioModel.query.all()
    niveis = NivelModel.query.all()

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        nivel = request.form.get('nivel')
        try:
            nivel = int(nivel)
        except (TypeError, ValueError):
            nivel = None

        if not nome or not email or not nivel:
            flash('Preencha todos os campos!', 'warning')
            return render_template('usuarios/usuarios.html', usuario=usuario, usuarios=usuarios, niveis=niveis)
        
        if UsuarioModel.query.filter(UsuarioModel.email == email , UsuarioModel.usuario_id != id).first():
            flash('Email já cadastrado!', 'error')
            return render_template('usuarios/usuarios.html', usuario=usuario, usuarios=usuarios, niveis=niveis)

        usuario.nome = nome
        usuario.email = email
        usuario.nivel_id = nivel
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))

    return render_template('usuarios/usuarios.html', usuario=usuario, usuarios=usuarios, niveis=niveis)


@usuarios_bp.route('/api/usuarios/<int:id>/alterar-senha', methods=['PUT'])
def alterar_senha_usuario(id):
    usuario = UsuarioModel.query.get_or_404(id)

    data = request.get_json(silent=True) or  {}
    nova_senha = data.get('nova_senha') or "default123"

    usuario.set_senha(nova_senha)
    usuario.primeiro_acesso = False  # Marca como não sendo o primeiro acesso
    db.session.commit()
    return {"message": "Senha alterada com sucesso!"}, 200


@usuarios_bp.route('/api/usuarios/<int:id>/desativar', methods=['POST'])
def desativar_nivel_usuario(id):
    if not current_user.is_admin():
        flash('Acesso negado!')
        return redirect(url_for('dashboard_bp.dashboard_view'))

    usuario = UsuarioModel.query.get_or_404(id)
    usuario.ativo = False
    db.session.commit()
    flash('Usuário desativado com sucesso!', 'success')
    return redirect(url_for('usuarios.listar_usuarios'))



@usuarios_bp.route('/api/usuarios/<int:id>/reativar', methods=['POST'])
def reativar_nivel_usuario(id):
    if not current_user.is_admin():
        flash('Acesso negado!')
        return redirect(url_for('dashboard_bp.dashboard_view'))
    usuario = UsuarioModel.query.get_or_404(id)
    usuario.ativo = True
    db.session.commit()
    flash('Usuário reativado com sucesso!', 'success')
    return redirect(url_for('usuarios.listar_usuarios'))