from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
login_manager = LoginManager()
admin = Admin(
    name="Painel Administrativo",

    theme=Bootstrap4Theme(
        swatch="darkly"
    )
)