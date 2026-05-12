from abc import ABC, abstractmethod

class ICategoria(ABC):
    
    @abstractmethod 
    def criar_categoria() -> None: pass
    
    @abstractmethod 
    def editar_categoria() -> None: pass
    
    @abstractmethod 
    def deletar_categoria() -> None: pass
    
    @abstractmethod 
    def listar_categoria() -> None: pass