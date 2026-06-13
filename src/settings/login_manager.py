from src.settings.extensions import login_manager
from src.models.usuario_model import Usuario


@login_manager.user_loader
def load_user(user_id):

    return Usuario.query.get(int(user_id))
