from abc import ABC, abstractmethod

class ICategoria(ABC):
    
    @abstractmethod 
    def criar_categoria() -> None: pass