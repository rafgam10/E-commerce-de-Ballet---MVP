from io import BytesIO

from PIL import Image

from src.models.categoria_model import Categoria
from src.models.produto_image import Produto_Images
from src.models.itens_carrinho import Itens_Carrinho
from src.models.ordens import Ordens, Status
from src.models.produto_model import Produto
from src.models.produto_variavel import Produto_Variavel
from src.models.repositories.usuario_repository import UsuarioRepository
from src.models.usuario_model import Role
from src.settings.extensions import db


def criar_produto_demo():
    categoria = Categoria(nome="Sapatilhas", slug="sapatilhas")
    db.session.add(categoria)
    db.session.flush()
    produto = Produto(
        nome="Sapatilha Rosa",
        slug="sapatilha-rosa",
        descricao="Sapatilha para treino.",
        price=99.90,
        ativo=True,
        categoria_id=categoria.id,
    )
    db.session.add(produto)
    db.session.flush()
    variacao = Produto_Variavel(
        tamanho="35",
        cor="Rosa",
        estoque=4,
        sku="SAPATILHA-ROSA-35",
        produto_id=produto.id,
    )
    db.session.add(variacao)
    db.session.commit()
    return {
        "produto_id": produto.id,
        "variacao_id": variacao.id,
        "price": produto.price,
    }


def registrar_cliente(client):
    return client.post(
        "/auth/register",
        data={
            "nome": "Cliente",
            "email": "cliente@example.com",
            "senha": "cliente123",
        },
        follow_redirects=True,
    )


def imagem_png_teste():
    arquivo = BytesIO()
    Image.new("RGB", (1, 1), color="white").save(arquivo, format="PNG")
    arquivo.seek(0)
    return arquivo


def test_catalogo_renderiza_produtos(app, client):
    with app.app_context():
        criar_produto_demo()

    response = client.get("/produtos")

    assert response.status_code == 200
    assert b"Sapatilha Rosa" in response.data


def test_fluxo_carrinho_checkout_pedido(app, client):
    with app.app_context():
        demo = criar_produto_demo()

    registrar_cliente(client)
    response = client.post(
        "/carrinho/adicionar",
        data={
            "produto_variavel_id": demo["variacao_id"],
            "quantidade": 2,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():
        item = Itens_Carrinho.query.first()
        assert item.quantidade == 2

    client.post(
        "/checkout/endereco",
        data={
            "rua": "Rua do Palco",
            "numero": 10,
            "cidade": "Sao Paulo",
            "estado": "SP",
            "cep": "01000-000",
            "pais": "Brasil",
        },
        follow_redirects=True,
    )

    response = client.post(
        "/checkout/confirmar",
        data={
            "endereco_id": 1,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Pedido #1" in response.data

    with app.app_context():
        pedido = Ordens.query.first()
        variacao_atualizada = db.session.get(Produto_Variavel, demo["variacao_id"])
        assert pedido.status == Status.PENDING.value
        assert pedido.preco_total == demo["price"] * 2
        assert variacao_atualizada.estoque == 2


def test_admin_protegido_redireciona_visitante(client):
    response = client.get("/admin/", follow_redirects=False)

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_admin_login_next_admin_login_redireciona_para_admin(app, client):
    with app.app_context():
        UsuarioRepository().criar_usuario(
            "Admin", "admin@example.com", "admin123", Role.ADMIN.value
        )
        criar_produto_demo()

    response = client.post(
        "/auth/login?next=http://127.0.0.1:5000/admin/login",
        data={"email": "admin@example.com", "senha": "admin123"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Painel Administrativo" in response.data
    assert b"Dashboard da Ballet Boutique" in response.data
    assert b"Pedidos pendentes" in response.data
    assert b"Baixo estoque" in response.data


def test_admin_tem_botao_sair_e_logout_funciona(app, client):
    with app.app_context():
        UsuarioRepository().criar_usuario(
            "Admin", "admin@example.com", "admin123", Role.ADMIN.value
        )

    client.post(
        "/auth/login",
        data={"email": "admin@example.com", "senha": "admin123"},
        follow_redirects=True,
    )
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b">Sair<" in response.data

    response = client.post("/admin/logout", follow_redirects=True)
    assert response.status_code == 200

    response = client.get("/admin/", follow_redirects=False)
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_admin_imagens_renderiza_upload(app, client):
    with app.app_context():
        UsuarioRepository().criar_usuario(
            "Admin", "admin@example.com", "admin123", Role.ADMIN.value
        )
        criar_produto_demo()

    client.post(
        "/auth/login",
        data={"email": "admin@example.com", "senha": "admin123"},
        follow_redirects=True,
    )
    response = client.get("/admin/produto_images/new/")

    assert response.status_code == 200
    assert b'type="file"' in response.data
    assert b"Sapatilha Rosa" in response.data
    assert b"&lt;Produto" not in response.data
    assert b"Dashboard da Ballet Boutique" not in response.data
    assert b'<div class="admin-dashboard">' not in response.data


def test_admin_imagens_salva_upload_local(app, client):
    with app.app_context():
        UsuarioRepository().criar_usuario(
            "Admin", "admin@example.com", "admin123", Role.ADMIN.value
        )
        demo = criar_produto_demo()

    client.post(
        "/auth/login",
        data={"email": "admin@example.com", "senha": "admin123"},
        follow_redirects=True,
    )
    response = client.post(
        "/admin/produto_images/new/",
        data={
            "produto": demo["produto_id"],
            "image_url": (imagem_png_teste(), "produto.png"),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    with app.app_context():
        imagem = Produto_Images.query.first()
        assert imagem.image_url.startswith("products/")

        response = client.get(f"/uploads/{imagem.image_url}")
        assert response.status_code == 200


def test_upload_folder_relativo_serve_arquivo():
    import os
    import shutil

    from src import create_app

    upload_folder = "uploads_test_tmp"
    shutil.rmtree(upload_folder, ignore_errors=True)
    try:
        app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "JWT_SECRET_KEY": "test-jwt-secret-with-at-least-32-bytes",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "WTF_CSRF_ENABLED": False,
                "UPLOAD_FOLDER": upload_folder,
            }
        )
        upload_file = os.path.join(app.config["UPLOAD_FOLDER"], "products", "teste.txt")

        with open(upload_file, "w", encoding="utf-8") as file:
            file.write("ok")

        response = app.test_client().get("/uploads/products/teste.txt")

        assert response.status_code == 200
        assert response.data == b"ok"
    finally:
        shutil.rmtree(upload_folder, ignore_errors=True)
