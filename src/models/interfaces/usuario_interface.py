from abc import ABC, abstractmethod

class UsuarioInterface(ABC):
    
    @abstractmethod
    def criar_usuario() -> None: pass
    
    @abstractmethod
    def get_usuario() -> None: pass
    
    @abstractmethod
    def get_all_usuarios() -> None: pass
    
    @abstractmethod
    def get_admin() -> None: pass
    
    @abstractmethod
    def get_all_admin() -> None: pass