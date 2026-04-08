from src.models.interfaces.produto_interface import IProduto
from src.models.produto_model import Produto
from src.models.categoria_model import Categoria
from src.settings.extensions import db

class ProdutoRepository(IProduto):
    
    def criar_produto(self, nome:str, slug:str, descricao:str, price:float, ativo:bool, categoria_id:int) -> None:
        novo_produto = Produto(
            nome, slug, descricao, price, ativo, categoria_id
        )
        db.session.add(novo_produto)
        db.session.commit()
    
    def editar_produto(self, id_produto: int, data: dict) -> None:
        produto = db.session.query(Produto).filter(Produto.id == id_produto).first()
        
        if not produto:
            raise Exception("Produto não encontrado")
        
        for key, value in data.items():
            if hasattr(produto, key):
                setattr(produto, key, value)
        
        db.session.commit()
        
    def deletar_produto(self, id_produto:int) -> None:
        produto = db.session.query(Produto).filter(Produto.id == id_produto).first()
        db.session.delete(produto)
        db.session.commit()