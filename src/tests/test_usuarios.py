from src import create_app
from src.models.repositories.usuario_repository import UsuarioRepository
from src.models.usuario_model import Role
from src.settings.extensions import db
import pytest

@pytest.mark.skip(reason="Passou")
def test_criar_usuario():
    
    app = create_app()
    
    with app.app_context():
        db.create_all()
        repo = UsuarioRepository()
        
        repo.criar_usuario(
            nome="teste1",
            email="teste@gmail.com",
            senha="teste123"
        )
      
@pytest.mark.skip(reason="Passou")  
def test_get_usuario():
    app = create_app()
    
    with app.app_context():
        db.create_all()
        repo = UsuarioRepository()
        
        response = repo.get_usuario(
            email="teste@gmail.com",
            senha="teste123"
        )
        
        print(response)
        assert response["nome"] == "teste1"
        assert response["role"] == "cliente"
        

@pytest.mark.skip("Passou")
def test_get_admin():
    
    app = create_app()
    
    with app.app_context():
        db.create_all()
        repo = UsuarioRepository()
        
        response = repo.get_admin(
            email="admin@gmail.com",
            senha="admin"
        )
        
        print(response)

@pytest.mark.skip(reason="Passou")        
def test_get_all_usuarios():
    
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        repo = UsuarioRepository()
        dict_usuarios = repo.get_all_usuarios()
        
        print(dict_usuarios)
        
@pytest.mark.skip(reason="Passou")        
def test_get_all_usuarios():
    
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        repo = UsuarioRepository()
        dict_usuarios = repo.get_all_admin()
        
        print(dict_usuarios)