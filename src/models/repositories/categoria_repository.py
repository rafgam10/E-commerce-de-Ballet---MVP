from src.models.interfaces.categoria_interface import ICategoria
from src.models.categoria_model import Categoria
from src.settings.extensions import db

class CategoriaRepository(ICategoria):
    
    def criar_categoria(self, nome, slug) -> None:
        nova_categoria = Categoria(nome, slug)
        db.session.add(nova_categoria)
        db.session.commit()