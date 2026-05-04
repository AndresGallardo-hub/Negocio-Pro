from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
# --- NUEVO: Iniciamos el gestor de sesiones de seguridad ---
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # --- NUEVO: Configuramos la seguridad ---
    login_manager.init_app(app)
    # Le decimos a Flask a dónde mandar al usuario si intenta entrar sin permiso
    login_manager.login_view = 'login' 
    login_manager.login_message = "Por favor, iniciá sesión para acceder a esta página."
    login_manager.login_message_category = "error"

    with app.app_context():
        from . import routes, models
        
        # --- NUEVO: Le enseñamos a Flask cómo buscar a tu usuario en la base de datos ---
        @login_manager.user_loader
        def load_user(user_id):
            return models.Usuario.query.get(int(user_id))
            
        db.create_all()

    return app