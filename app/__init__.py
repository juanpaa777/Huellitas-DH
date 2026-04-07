"""app/__init__.py — Application Factory."""
import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .models import db, bcrypt, User
from config import config_map

migrate    = Migrate()
login_mgr  = LoginManager()
csrf       = CSRFProtect()          # ← FIX: inicializar CSRF globalmente

login_mgr.login_view         = "auth.login"
login_mgr.login_message      = "Inicia sesión para acceder a esta página."
login_mgr.login_message_category = "warning"


def create_app(env: str = None) -> Flask:
    app = Flask(__name__, instance_relative_config=False)

    env = env or os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config_map.get(env, config_map["development"]))

    # Extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_mgr.init_app(app)
    csrf.init_app(app)              # ← FIX: registrar con la app

    @login_mgr.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Blueprints
    from .blueprints.main.routes      import main_bp
    from .blueprints.auth.routes      import auth_bp
    from .blueprints.pets.routes      import pets_bp
    from .blueprints.adoptions.routes import adoptions_bp
    from .blueprints.admin.routes     import admin_bp
    from .blueprints.rescuer.routes   import rescuer_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,      url_prefix="/auth")
    app.register_blueprint(pets_bp,      url_prefix="/mascotas")
    app.register_blueprint(adoptions_bp, url_prefix="/adopciones")
    app.register_blueprint(admin_bp,     url_prefix="/admin")
    app.register_blueprint(rescuer_bp,   url_prefix="/rescatista")

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Inyectar utils en Jinja2
    from .utils import STATUS_COLOR
    app.jinja_env.globals["STATUS_COLOR"] = STATUS_COLOR

    # Error handlers
    from .blueprints.main.routes import page_not_found, server_error, forbidden
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    return app
