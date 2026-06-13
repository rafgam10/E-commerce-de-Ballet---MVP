from src.models.repositories.categoria_repository import CategoriaRepository


def test_criar_editar_listar_categoria(app):
    with app.app_context():
        repo = CategoriaRepository()
        categoria = repo.criar_categoria("Sapatilhas", "sapatilhas")
        atualizada = repo.editar_categoria(
            categoria.id, {"nome": "Sapatilhas de Ballet"}
        )
        lista = repo.listar_categoria()

        assert atualizada.nome == "Sapatilhas de Ballet"
        assert lista[0].slug == "sapatilhas"


def test_deletar_categoria(app):
    with app.app_context():
        repo = CategoriaRepository()
        categoria = repo.criar_categoria("Saias", "saias")

        deletada = repo.deletar_categoria(categoria.id)

        assert deletada.id == categoria.id
