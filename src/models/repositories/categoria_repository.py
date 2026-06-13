from src.models.interfaces.categoria_interface import ICategoria
from src.models.categoria_model import Categoria
from src.settings.extensions import db


class CategoriaRepository(ICategoria):

    def criar_categoria(self, nome, slug) -> Categoria:
        nova_categoria = Categoria(nome, slug)
        db.session.add(nova_categoria)
        db.session.commit()
        return nova_categoria

    def editar_categoria(self, id: int, data: dict) -> Categoria:
        categoria = db.session.get(Categoria, id)
        if not categoria:
            raise Exception("Categoria não encontrada")

        if data.get("nome") is not None:
            categoria.nome = data.get("nome")
        if data.get("slug") is not None:
            categoria.slug = data.get("slug")

        db.session.commit()
        return categoria

    def deletar_categoria(self, id: int) -> Categoria:
        categoria = db.session.get(Categoria, id)
        if not categoria:
            raise Exception("Categoria não encontrada")

        db.session.delete(categoria)
        db.session.commit()
        return categoria

    def listar_categoria(self) -> list[Categoria]:
        lista = db.session.query(Categoria).all()
        return lista
