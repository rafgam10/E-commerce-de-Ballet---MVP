import os
from uuid import uuid4

from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask import current_app
from markupsafe import Markup
from werkzeug.utils import secure_filename

from src.settings.extensions import admin, db
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


class UsuarioAdminView(ModelView):
    can_create = False
    column_exclude_list = ["senha"]
    form_excluded_columns = ["senha", "enderecos", "carrinhos", "ordens"]
    column_searchable_list = ["nome", "email"]
    column_filters = ["role", "created_at"]


class ProdutoAdminView(ModelView):
    column_searchable_list = ["nome", "slug"]
    column_filters = ["ativo", "categoria_id", "created_at"]


def produto_image_upload_path():
    return os.path.abspath(current_app.config["UPLOAD_FOLDER"])


def produto_image_namegen(obj, file_data):
    filename = secure_filename(file_data.filename or "produto")
    _, extension = os.path.splitext(filename)
    return f"{uuid4().hex}{extension.lower()}"


def image_preview_formatter(view, context, model, name):
    if not model.url:
        return ""
    return Markup(
        f'<img src="{model.url}" alt="Imagem do produto" '
        'style="max-height: 80px; border-radius: 8px;">'
    )


class ProdutoImagemAdminView(ModelView):
    column_list = ["id", "produto", "preview", "image_url"]
    column_labels = {
        "image_url": "Imagem",
        "produto": "Produto",
        "preview": "Preview",
    }
    column_formatters = {"preview": image_preview_formatter}
    form_columns = ["produto", "image_url"]
    form_extra_fields = {
        "image_url": ImageUploadField(
            "Imagem do produto",
            base_path=produto_image_upload_path,
            relative_path="products/",
            endpoint="uploaded_file",
            allowed_extensions=("jpg", "jpeg", "png", "webp"),
        )
    }


class PedidoAdminView(ModelView):
    can_create = False
    column_filters = ["status", "created_at"]
    column_searchable_list = ["status"]


class EstoqueAdminView(ModelView):
    column_searchable_list = ["sku", "cor", "tamanho"]
    column_filters = ["tamanho", "cor", "estoque"]


def configurar_admin():
    if getattr(admin, "_ballet_views_configured", False):
        return

    admin.add_view(UsuarioAdminView(Usuario, db, name="Usuarios"))
    admin.add_view(ModelView(Endereco, db, name="Enderecos"))
    admin.add_view(ModelView(Categoria, db, name="Categorias"))
    admin.add_view(ProdutoAdminView(Produto, db, name="Produtos"))
    admin.add_view(EstoqueAdminView(Produto_Variavel, db, name="Variacoes"))
    admin.add_view(ProdutoImagemAdminView(Produto_Images, db, name="Imagens"))
    admin.add_view(ModelView(Carrinhos, db, name="Carrinhos"))
    admin.add_view(ModelView(Itens_Carrinho, db, name="Itens do carrinho"))
    admin.add_view(PedidoAdminView(Ordens, db, name="Pedidos"))
    admin.add_view(ModelView(Itens_Order, db, name="Itens dos pedidos"))
    admin._ballet_views_configured = True
