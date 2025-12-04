from flask import Blueprint, request, jsonify
from models import Cliente
from database import db
import bcrypt
import random
from datetime import datetime, timedelta

cliente_bp = Blueprint('cliente', __name__)

codigos_temporales = []

@cliente_bp.route("/registrar", methods=["POST"])
def registrar():
    data = request.get_json()

    if Cliente.buscar_por_correo(data["correo"]):
        return jsonify({"ok": False, "message": "Correo ya registrado"}), 409

    password_hash = bcrypt.hashpw(data["passwordd"].encode('utf-8'), bcrypt.gensalt())

    nuevo = Cliente(
        nombres=data["nombres"],
        correo=data["correo"],
        password_hash=password_hash
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({
        "ok": True,
        "content": {"id": nuevo.id, "nombre": nuevo.nombres},
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

    codigos_temporales.append({
        "id": cliente.id,
        "codigo": codigo,
        "expira": caducidad
    })

    return jsonify({
        "ok": True,
        "codigo_simulado": codigo,
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
