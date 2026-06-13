import click

from src.models.categoria_model import Categoria
from src.models.produto_model import Produto
from src.models.produto_variavel import Produto_Variavel
from src.models.repositories.usuario_repository import UsuarioRepository
from src.models.usuario_model import Role
from src.settings.extensions import db
from src.utils.slug_util import gerar_slug


def register_commands(app):
    @app.cli.command("create-admin")
    @click.option("--nome", prompt=True)
    @click.option("--email", prompt=True)
    @click.option("--senha", prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(nome, email, senha):
        repo = UsuarioRepository()
        usuario = repo.criar_usuario(nome, email, senha, Role.ADMIN.value)
        click.echo(f"Admin criado: {usuario.email}")

    @app.cli.command("seed-demo")
    def seed_demo():
        categorias = ["Sapatilhas", "Collants", "Saias", "Acessórios"]
        categorias_por_nome = {}

        for nome in categorias:
            slug = gerar_slug(nome)
            categoria = Categoria.query.filter_by(slug=slug).first()
            if not categoria:
                categoria = Categoria(nome=nome, slug=slug)
                db.session.add(categoria)
            categorias_por_nome[nome] = categoria

        db.session.flush()

        produtos = [
            {
                "nome": "Sapatilha Meia Ponta Rosa",
                "categoria": "Sapatilhas",
                "descricao": "Sapatilha confortável para aulas e ensaios.",
                "price": 89.90,
                "variacoes": [("34", "Rosa", 8), ("35", "Rosa", 6), ("36", "Rosa", 4)],
            },
            {
                "nome": "Collant Manga Curta Preto",
                "categoria": "Collants",
                "descricao": "Collant básico para treino com tecido macio.",
                "price": 129.90,
                "variacoes": [("P", "Preto", 7), ("M", "Preto", 9), ("G", "Preto", 5)],
            },
            {
                "nome": "Saia Envelope Lilás",
                "categoria": "Saias",
                "descricao": "Saia leve para composição de aula e apresentação.",
                "price": 74.90,
                "variacoes": [("P", "Lilás", 5), ("M", "Lilás", 5)],
            },
        ]

        for item in produtos:
            slug = gerar_slug(item["nome"])
            produto = Produto.query.filter_by(slug=slug).first()
            if not produto:
                produto = Produto(
                    nome=item["nome"],
                    slug=slug,
                    descricao=item["descricao"],
                    price=item["price"],
                    ativo=True,
                    categoria_id=categorias_por_nome[item["categoria"]].id,
                )
                db.session.add(produto)
                db.session.flush()

            for tamanho, cor, estoque in item["variacoes"]:
                sku = gerar_slug(f"{item['nome']} {tamanho} {cor}").upper()
                variacao = Produto_Variavel.query.filter_by(sku=sku).first()
                if not variacao:
                    db.session.add(
                        Produto_Variavel(
                            tamanho=tamanho,
                            cor=cor,
                            estoque=estoque,
                            sku=sku,
                            produto_id=produto.id,
                        )
                    )

        db.session.commit()
        click.echo("Dados de demonstração criados.")
