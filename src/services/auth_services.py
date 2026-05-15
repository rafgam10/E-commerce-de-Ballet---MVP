import bcrypt

from flask_jwt_extended import create_access_token

from src.models.repositories.usuario_repository import UsuarioRepository

class AuthService:
    
    @staticmethod
    def login(email, senha):
        repo =  UsuarioRepository()
        usuario = repo.get_usuario(email)
        
        if not usuario:
            raise Exception("Usuário não encontrado")
        
        senha_correta = bcrypt.checkpw(
            senha.encode(),
            usuario.senha.encode()
        )
        
        if not senha_correta:
            raise Exception("Senha inválida")
        
        token = create_access_token(
            identity=str(usuario.id),
            additional_claims={
                "role": usuario.role
            }
        )
        
        return {
            "access_token": token,
            "usuario": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "role": usuario.role
            }
        }
    
    
    @staticmethod
    def cadastro(nome, email, senha):
        repo = UsuarioRepository()
        usuario = repo.criar_usuario(nome, email, senha)
        
        return {
            "usuario": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "senha": usuario.senha,
                "role": usuario.role,
                "created_at": usuario.created_at
            }
        }