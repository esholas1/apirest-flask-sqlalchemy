from flask import Blueprint, request, jsonify
from models import clientes, codigos_temporales, Cliente
import bcrypt
import random
from datetime import datetime, timedelta

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route("/registrar", methods=["POST"])
def registrar():
    data = request.get_json()
    if Cliente.buscar_por_correo(data["correo"]):
        return jsonify({"ok": False, "message": "Correo ya registrado"}), 409

    password_hash = bcrypt.hashpw(data["passwordd"].encode('utf-8'), bcrypt.gensalt())
    nuevo_cliente = Cliente(len(clientes)+1, data["nombres"], data["correo"], password_hash)

    clientes.append(nuevo_cliente)

    return jsonify({
        "ok": True,
        "content": {"id": nuevo_cliente.id, "nombre": nuevo_cliente.nombres},
        "message": "Cliente registrado correctamente"
    }), 201

@cliente_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    cliente = Cliente.buscar_por_correo(data["correo"])

    if not cliente or not cliente.verificar_password(data["passwordd"]):
        return jsonify({"ok": False, "message": "Credenciales incorrectas"}), 401

    return jsonify({
        "ok": True,
        "content": {
            "id": cliente.id,
            "nombres": cliente.nombres,
            "correo": cliente.correo
        },
        "message": "Login exitoso"
    })

@cliente_bp.route("/enviar-codigo", methods=["POST"])
def enviar_codigo():
    data = request.get_json()
    cliente = Cliente.buscar_por_correo(data["correo"])

    if not cliente:
        return jsonify({"ok": False, "message": "Correo no registrado"}), 404

    codigo = random.randint(1000, 9999)
    caducidad = datetime.now() + timedelta(minutes=5)

    codigos_temporales.append({"id": cliente.id, "codigo": codigo, "expira": caducidad})

    return jsonify({
        "ok": True,
        "codigo": codigo,
        "message": "Código enviado"
    })

@cliente_bp.route("/validar-codigo", methods=["POST"])
def validar_codigo():
    data = request.get_json()

    registro = next((c for c in codigos_temporales
                     if c["id"] == data["cliente_id"] and c["codigo"] == data["codigo"]),
                    None)

    if not registro:
        return jsonify({"ok": False, "message": "Código incorrecto"}), 401

    if datetime.now() > registro["expira"]:
        return jsonify({"ok": False, "message": "Código expirado"}), 410

    return jsonify({"ok": True, "message": "Código validado correctamente"})
