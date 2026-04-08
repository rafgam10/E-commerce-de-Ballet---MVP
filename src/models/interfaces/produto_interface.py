from abc import ABC, abstractmethod

class IProduto(ABC):
    
    @abstractmethod
    def criar_produto() -> None: pass
    
    @abstractmethod
    def editar_produto() -> None: pass
    
    @abstractmethod
    def deletar_produto() -> None: pass