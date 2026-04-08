from abc import ABC, abstractmethod

class IProduto(ABC):
    
    @abstractmethod
    def criar_produto() -> None: pass
    
    @abstractmethod
    def editar_produto() -> None: pass
    
    @abstractmethod
    def deletar_produto() -> None: pass
    
    @abstractmethod
    def adicionar_img_produto() -> None: pass
    
    @abstractmethod
    def criar_variaveis_produto() -> None: pass