import bcrypt

from src.models.interfaces.usuario_interface import UsuarioInterface
from src.models.usuario_model import Usuario, Role
from src.settings.extensions import db


class UsuarioRepository(UsuarioInterface):

    def criar_usuario(self, nome: str, email: str, senha: str, role=Role.CLIENTE.value) -> Usuario:
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
        
        usuario = Usuario(nome, email, senha_hash, role)

        db.session.add(usuario)
        db.session.commit()

        return usuario

    def recuperar_senha(self, email:str, nova_senha:str):
        usuario = db.session.query(Usuario).filter(Usuario.email == email).first()
        
        usuario.senha = nova_senha
        db.session.commit()
        return usuario
    
    def atualizar_usuario(self):
        ...
    
    def get_usuario(self, email: str):

        usuario = db.session.query(Usuario).filter(
            Usuario.email == email
        ).first()

        return usuario

    def get_all_usuarios(self) -> list[dict]:

        usuarios = db.session.query(Usuario).all()
        return [user.__to_dict__() for user in usuarios]

    def get_admin(self, email: str):

        admin = db.session.query(Usuario).filter(
            Usuario.email == email,
            Usuario.role == Role.ADMIN.value
        ).first()

        if admin:
            return admin.__to_dict__()

        return None

    def get_all_admin(self) -> list[dict]:

        admins = db.session.query(Usuario).filter(
            Usuario.role == Role.ADMIN.value
        ).all()

        return [admin.__to_dict__() for admin in admins]