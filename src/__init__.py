from flask import Flask, flash, redirect, request, send_from_directory, url_for
from flask_login import current_user
from .settings.config import Config
from .settings.extensions import admin as flask_admin_ext
from .settings.extensions import csrf, db, jwt, login_manager, migrate

import os


def create_app(config_object=None):
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )
    app.config.from_object(Config)
    if isinstance(config_object, dict):
        app.config.update(config_object)
    elif config_object is not None:
        app.config.from_object(config_object)

    configurar_upload_folder(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    flask_admin_ext.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para continuar."

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

    # Import Flask_Login
    from src.settings.login_manager import load_user

    # Import Admin views:
    from src.admin.views import configurar_admin

    configurar_admin()
    proteger_admin(app)
    registrar_uploads(app)
    registrar_template_helpers(app)
    from src.commands import register_commands

    register_commands(app)

    # Importações de Blueprintes:
    from src.routes.auth_route import auth_bp
    from src.routes.admin_route import admin_bp
    from src.routes.store_route import store_bp

    app.register_blueprint(store_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app


def proteger_admin(app):
    @app.before_request
    def restringir_admin():
        if not request.path.startswith("/admin") or request.path.startswith(
            "/admin/static"
        ):
            return None

        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))

        if current_user.role != "admin":
            flash("Acesso restrito a administradores.", "danger")
            return redirect(url_for("store.home"))

        return None


def configurar_upload_folder(app):
    upload_folder = app.config["UPLOAD_FOLDER"]
    if not os.path.isabs(upload_folder):
        project_root = os.path.abspath(os.path.join(app.root_path, ".."))
        upload_folder = os.path.join(project_root, upload_folder)

    app.config["UPLOAD_FOLDER"] = upload_folder
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(os.path.join(upload_folder, "products"), exist_ok=True)


def registrar_uploads(app):
    @app.get("/uploads/<path:filename>", endpoint="uploaded_file")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


def registrar_template_helpers(app):
    @app.template_filter("brl")
    def brl(valor):
        valor = valor or 0
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @app.context_processor
    def contexto_global():
        quantidade = 0
        if current_user.is_authenticated:
            from src.models.repositories.carrinho_repository import CarrinhoRepository

            resumo = CarrinhoRepository().resumir_carrinho(current_user.id)
            quantidade = resumo["quantidade_itens"]

        return {"cart_count": quantidade, "admin_dashboard": admin_dashboard}


def admin_dashboard():
    from sqlalchemy import func

    from src.models.carrinho_model import Carrinhos, CartStatus
    from src.models.ordens import Ordens, Status
    from src.models.produto_model import Produto
    from src.models.produto_variavel import Produto_Variavel
    from src.models.usuario_model import Role, Usuario

    faturamento = (
        db.session.query(func.coalesce(func.sum(Ordens.preco_total), 0))
        .filter(Ordens.status != Status.CANCELLED.value)
        .scalar()
        or 0
    )
    status_counts = {
        status.value: Ordens.query.filter(Ordens.status == status.value).count()
        for status in Status
    }

    return {
        "pedidos_pendentes": status_counts[Status.PENDING.value],
        "pedidos_pagos": status_counts[Status.PAID.value],
        "faturamento": faturamento,
        "clientes": Usuario.query.filter(Usuario.role == Role.CLIENTE.value).count(),
        "produtos_ativos": Produto.query.filter(Produto.ativo.is_(True)).count(),
        "carrinhos_ativos": Carrinhos.query.filter(
            Carrinhos.status == CartStatus.ATIVO.value
        ).count(),
        "status_counts": status_counts,
        "pedidos_recentes": Ordens.query.order_by(Ordens.created_at.desc())
        .limit(6)
        .all(),
        "estoque_baixo": Produto_Variavel.query.filter(Produto_Variavel.estoque <= 3)
        .order_by(Produto_Variavel.estoque.asc())
        .limit(6)
        .all(),
        "produtos_sem_imagem": Produto.query.filter(~Produto.images.any())
        .order_by(Produto.nome.asc())
        .limit(6)
        .all(),
    }
