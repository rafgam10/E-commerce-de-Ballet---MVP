from src.models.interfaces.categoria_interface import ICategoria
from src.models.categoria_model import Categoria
from src.settings.extensions import db

class CategoriaRepository(ICategoria):
    
    def criar_categoria(self, nome, slug) -> None:
        nova_categoria = Categoria(nome, slug)
        db.session.add(nova_categoria)
        db.session.commit()
        
    def editar_categoria(self, id:int, data:dict) -> None:
        categoria = db.session.query(Categoria).filter(Categoria.id == id).first()
        categoria.nome = data.get("nome")
        categoria.slug = data.get("slug")
        db.session.commit()
        return categoria
    
    def deletar_categoria(self, id:int) -> None:
        categoria = db.session.query(Categoria).filter(Categoria.id == id).first()
        db.session.delete(categoria)
        db.session.commit()
        return categoria
    
    def listar_categoria(self) -> list[Categoria]:
        lista = db.session.query(Categoria).all()
        return lista