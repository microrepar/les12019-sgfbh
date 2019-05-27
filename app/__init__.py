from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# codigo de teste do Blueprint ########################################
db = SQLAlchemy(session_options={"autoflush": False})
migrate = Migrate()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'O login é necessário para acessar esta página!'
login.login_message_category = 'success'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.bp_autenticacao import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.bp_aplicacao import bp as aplicacao_bp
    app.register_blueprint(aplicacao_bp)

    from app.bp_endereco import bp as end_bp
    app.register_blueprint(end_bp)

    from app.bp_frequencia import bp as frequencia_bp
    app.register_blueprint(frequencia_bp)

    from app.bp_funcionario import bp as func_bp
    app.register_blueprint(func_bp)

    from app.bp_escala import bp as escala_bp
    app.register_blueprint(escala_bp)

    from app.bp_main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.bp_ocorrencia import bp as ocorrencia_bp
    app.register_blueprint(ocorrencia_bp)

    from app.bp_ponto import bp as ponto_bp
    app.register_blueprint(ponto_bp)

    # from app.bp_relogioponto import bp as relogioponto_bp
    # app.register_blueprint(relogioponto_bp)

    from app.bp_solicitacao import bp as solicitacao_bp
    app.register_blueprint(solicitacao_bp)

    return app


# codigo de teste do Blueprint ########################################


# app = Flask(__name__)
# app.config.from_object(Config)

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)


# from app import routes, controle, viewhelper, command
# from les12019_dominio import models
# from les12019_core import utils, aplicacao
