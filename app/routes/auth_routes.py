from flask import Blueprint, redirect, url_for , request, flash , render_template
from flask_login import current_user, login_user, logout_user, login_required
from app.models.usuario_model import UsuarioModel
from app import db


# Cria o blueprint de autenticação
# Esse blueprint vai conter as rotas de autenticação, como login, logout e alterar senha
auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
        # se meu metodo for POST , vou pegar os dados do form
        email = request.form.get('email')
        password = request.form.get('password')
        # to fazendo a validação dos campos se tiver algo errado retorna o template de login
        if not email or not password:
            flash('Preencha todos os campos!', 'warning')
            return render_template('auth/login.html')
        # agora apos a vailidação, vou buscar o usuário no banco de dados
        usuario = UsuarioModel.query.filter_by(email=email).first()
        #aqui eu verifico se o usuário existe e se a senha está correta
        # se o usuário existir e a senha estiver correta, eu faço o login
        # se não, eu retorno uma mensagem de erro
        if usuario and usuario.check_senha(password):
            login_user(usuario)
            return redirect(url_for('auth.test'))  # Por enquanto redireciona para o test
        else:
            flash('Email ou senha inválidos!', 'error')
            return render_template('auth/login.html')
   # Se for GET, mostra o formulário de login
   return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/alterar-senha', methods=['GET', 'POST'])

def alterar_senha():
    if request.method == 'POST':
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')
        if not senha_atual or not nova_senha or not confirmar_senha:
            flash('Preencha todos os campos!', 'warning')
            return render_template('auth/alterar_senha.html')
        
        if nova_senha != confirmar_senha:
            flash('As novas senhas não coincidem!', 'error')
            return render_template('auth/alterar_senha.html')

        if not current_user.check_senha(senha_atual):
            flash('Senha atual incorreta!', 'error')
            return render_template('auth/alterar_senha.html')


        current_user.set_senha(nova_senha)
        db.commit()
        flash('Senha alterada com sucesso!, faça login novamente.', 'success')
        return redirect(url_for('auth.login'))  # Redireciona para mostrar a mensagem
    
    # Se for GET, mostra o formulário
    return render_template('auth/alterar_senha.html')