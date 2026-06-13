from src.models.repositories.usuario_repository import UsuarioRepository
from src.models.usuario_model import Role
import bcrypt


def test_criar_usuario_com_hash(app):
    with app.app_context():
        repo = UsuarioRepository()
        usuario = repo.criar_usuario("Teste", "teste@example.com", "teste123")

        assert usuario.id is not None
        assert usuario.senha != "teste123"
        assert bcrypt.checkpw("teste123".encode(), usuario.senha.encode())


def test_recuperar_senha_recria_hash(app):
    with app.app_context():
        repo = UsuarioRepository()
        repo.criar_usuario("Teste", "teste@example.com", "teste123")
        usuario = repo.recuperar_senha("teste@example.com", "nova123")

        assert bcrypt.checkpw("nova123".encode(), usuario.senha.encode())


def test_get_admin(app):
    with app.app_context():
        repo = UsuarioRepository()
        repo.criar_usuario("Admin", "admin@example.com", "admin123", Role.ADMIN.value)
        admin = repo.get_admin("admin@example.com")

        assert admin["role"] == Role.ADMIN.value
        assert "senha" not in admin


def test_cadastro_web_loga_usuario(client):
    response = client.post(
        "/auth/register",
        data={
            "nome": "Cliente",
            "email": "cliente@example.com",
            "senha": "cliente123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Escolhas para come" in response.data


def test_login_json_retorna_token(app, client):
    with app.app_context():
        repo = UsuarioRepository()
        repo.criar_usuario("Cliente", "cliente@example.com", "cliente123")

    response = client.post(
        "/auth/login",
        json={
            "email": "cliente@example.com",
            "senha": "cliente123",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.get_json()
