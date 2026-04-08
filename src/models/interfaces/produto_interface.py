from abc import ABC, abstractmethod

class IProduto(ABC):
    
    @abstractmethod
    def criar_produto() -> None: pass