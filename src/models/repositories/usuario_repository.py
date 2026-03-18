from src.models.interfaces.usuario_interface import UsuarioInterface
from src.models.usuario_model import Usuario, Role
from src.settings.extensions import db


class UsuarioRepository(UsuarioInterface):

    def criar_usuario(self, nome: str, email: str, senha: str, role=Role.CLIENTE.value) -> Usuario:
        usuario = Usuario(nome, email, senha, role)

        db.session.add(usuario)
        db.session.commit()

        return usuario

    def get_usuario(self, email: str, senha: str):

        usuario_select = db.session.query(Usuario).filter(
            Usuario.email == email,
            Usuario.senha == senha
        ).first()

        if usuario_select:
            return usuario_select.__to_dict__()

        return None

    def get_all_usuarios(self) -> list[dict]:

        usuarios = db.session.query(Usuario).all()
        return [user.__to_dict__() for user in usuarios]

    def get_admin(self, email: str, senha: str):

        admin = db.session.query(Usuario).filter(
            Usuario.email == email,
            Usuario.senha == senha,
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