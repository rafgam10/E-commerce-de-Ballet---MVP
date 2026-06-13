from src.models.repositories.endereco_repository import Endereco_Repository
from src.models.repositories.usuario_repository import UsuarioRepository


def test_cadastra_lista_edita_remove_endereco(app):
    with app.app_context():
        usuario = UsuarioRepository().criar_usuario(
            "Cliente", "cliente@example.com", "cliente123"
        )
        repo = Endereco_Repository()
        endereco = repo.cadastrar_endereco(
            rua="Rua dos Ensaios",
            numero=80,
            cidade="Sao Luis",
            estado="MA",
            cep="65000000",
            user_id=usuario.id,
        )

        repo.editar_endereco(endereco.id, {"numero": 81})
        lista = repo.listar_endereco(usuario.id)
        removido = repo.remover_endereco(endereco.id)

        assert lista[0]["numero"] == 81
        assert lista[0]["cep"] == "65000-000"
        assert removido.id == endereco.id


def test_cadastrar_endereco_aceita_cep_com_hifen(app):
    with app.app_context():
        usuario = UsuarioRepository().criar_usuario(
            "Cliente", "cliente2@example.com", "cliente123"
        )
        endereco = Endereco_Repository().cadastrar_endereco(
            rua="Rua C",
            numero=304,
            cidade="Dom Pedro",
            estado="MA",
            cep="65765-000",
            user_id=usuario.id,
        )

        assert endereco.cep == "65765-000"
