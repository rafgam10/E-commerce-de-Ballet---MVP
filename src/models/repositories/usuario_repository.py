import bcrypt

from src.models.interfaces.usuario_interface import UsuarioInterface
from src.models.usuario_model import Usuario, Role
from src.settings.extensions import db


class UsuarioRepository(UsuarioInterface):

    def criar_usuario(
        self, nome: str, email: str, senha: str, role=Role.CLIENTE.value
    ) -> Usuario:
        if self.get_usuario(email):
            raise Exception("E-mail já cadastrado")

        role_value = role.value if isinstance(role, Role) else role
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

        usuario = Usuario(nome, email, senha_hash, role_value)

        db.session.add(usuario)
        db.session.commit()

        return usuario

    def recuperar_senha(self, email: str, nova_senha: str):
        usuario = db.session.query(Usuario).filter(Usuario.email == email).first()
        if not usuario:
            raise Exception("Usuário não encontrado")

        usuario.senha = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()
        db.session.commit()
        return usuario

    def atualizar_usuario(self, id_usuario: int, data: dict):
        usuario = db.session.get(Usuario, id_usuario)
        if not usuario:
            raise Exception("Usuário não encontrado")

        for campo in ("nome", "email", "role"):
            if campo in data and data[campo] is not None:
                setattr(usuario, campo, data[campo])

        if data.get("senha"):
            usuario.senha = bcrypt.hashpw(
                data["senha"].encode(), bcrypt.gensalt()
            ).decode()

        db.session.commit()
        return usuario

    def get_usuario(self, email: str):

        usuario = db.session.query(Usuario).filter(Usuario.email == email).first()

        return usuario

    def get_all_usuarios(self) -> list[dict]:

        usuarios = db.session.query(Usuario).all()
        return [user.__to_dict__() for user in usuarios]

    def get_admin(self, email: str):

        admin = (
            db.session.query(Usuario)
            .filter(Usuario.email == email, Usuario.role == Role.ADMIN.value)
            .first()
        )

        if admin:
            return admin.__to_dict__()

        return None

    def get_all_admin(self) -> list[dict]:

        admins = (
            db.session.query(Usuario).filter(Usuario.role == Role.ADMIN.value).all()
        )

        return [admin.__to_dict__() for admin in admins]
