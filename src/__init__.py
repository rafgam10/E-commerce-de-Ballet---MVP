from flask import Flask
from .settings.config import Config
from .settings.extensions import db, migrate, login_manager

import os

def create_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )
    app.config.from_object(Config)
    
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Importações de Models:
    from src.models.usuario_model import Usuario
    from src.models.endereco_model import Endereco
    from src.models.categoria_model import Categoria
    from src.models.produto_model import Produto
    from src.models.produto_variavel import Produto_Variavel
    from src.models.produto_image import Produto_Images
    from src.models.carrinho_model import Carrinhos
    from src.models.itens_carrinho import Itens_Carrinho
    from src.models.ordens import Ordens
    from src.models.itens_order import Itens_Order
        
    # Importações de Blueprintes:
    from src.routes.auth_route import auth_bp
    
    app.register_blueprint(auth_bp)


    return app
