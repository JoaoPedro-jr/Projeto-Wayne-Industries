# imports do Flask e extensões
# eu importei as extensões que vou usar se precisar de mais só importar aqui
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# aqui eu estou criando as instâncias 
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
bcrypt = Bcrypt()

# aqui eu estou criando a aplicação Flask
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')# aqui eu estou carregando as configurações da aplicação

    # aqui eu conecto as instâncias com a aplicação Flask
    # tambem estou conectando as extensões com a aplicação Flask
    db.init_app(app)    
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    login_manager.login_view = 'auth.login'  # Define a rota de login
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'  #se alguem tentar acessar uma rota protegida
    login_manager.login_message_category = 'warning'  # Categoria da mensagem

    from app.routes.auth_routes import auth_bp
    from app.routes.main_routes import index_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.usuarios_routes import usuarios_bp
    from app.routes.niveis_routes import niveis_bp
    from app.routes.recursos_routes import recursos_bp
    from app.routes.logs_routes import logs_bp
    app.register_blueprint(auth_bp, url_prefix='/auth') # Registra o blueprint de autenticação
    app.register_blueprint(index_bp, url_prefix='/')  # Registra o blueprint principal
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')  # Registra o blueprint do dashboard
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')  # Registra o blueprint de usuários
    app.register_blueprint(niveis_bp, url_prefix='/niveis')  # Registra o blueprint de níveis
    app.register_blueprint(recursos_bp, url_prefix='/recursos')  # Registra o blueprint de recursos
    app.register_blueprint(logs_bp, url_prefix='/logs')  # Registra o blueprint de logs

    return app


# Carregando o usuário
@login_manager.user_loader
def load_user(user_id):
    from app.models.usuario_model import UsuarioModel
    return UsuarioModel.query.get(int(user_id))