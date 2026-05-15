from flask import Blueprint, request, jsonify, flash
from src.settings.extensions import db

from src.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
controller = AuthController()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    try:
        
        data = request.get_json()
        
        response =  controller.login(data)
        
        return jsonify(response), 200
         
    except Exception as e:
        return jsonify({
            "msg": str(e)
        }), 400
    

@auth_bp.route("/logout", methods=["POST"])
def logout():

    return jsonify({
        "msg": "Logout realizado com sucesso"
    }), 200
    
    
@auth_bp.route("/register", methods=["GET","POST"])
def cadastro_usuario():
    try:
        data = request.get_json()
        
        usuario = controller.cadastro_usuario_cliente(data)
        
        return jsonify({
            "msg": "Usuario criando com sucesso."
        }), 201
        
    except Exception as e:
        return jsonify({
            "msg": str(e)
        }), 400
