from src.models.repositories.produto_repository import ProdutoRepository
from src.models.categoria_model import Categoria
from src.models.produto_model import Produto
from src.settings.extensions import db


def test_criar_editar_produto(app):
    with app.app_context():
        repo = ProdutoRepository()
        categoria = Categoria(nome="Ballet", slug="ballet")
        db.session.add(categoria)
        db.session.commit()

        produto = repo.criar_produto(
            nome="Tutu",
            slug="tutu",
            descricao="roupa normal",
            price=89.99,
            ativo=True,
            categoria_id=categoria.id,
        )
        repo.editar_produto(
            produto.id, {"nome": "Tutu Premium", "price": 120.0, "ativo": False}
        )

        produto_atualizado = db.session.get(Produto, produto.id)

        assert produto_atualizado.nome == "Tutu Premium"
        assert produto_atualizado.price == 120.0
        assert produto_atualizado.ativo is False


def test_imagem_variacao_e_delete_produto(app):
    with app.app_context():
        repo = ProdutoRepository()
        categoria = Categoria(nome="Ballet", slug="ballet")
        db.session.add(categoria)
        db.session.commit()
        produto = repo.criar_produto(
            "Tutu", "tutu", "roupa normal", 89.99, True, categoria.id
        )

        imagem = repo.adicionar_img_produto("/static/tutu.jpg", produto.id)
        variacao = repo.criar_variaveis_produto(
            "M", "Azul", 10, "TUTU-AZUL-M", produto.id
        )
        deletado = repo.deletar_produto(produto.id)

        assert imagem.id is not None
        assert variacao.estoque == 10
        assert deletado.id == produto.id
