import bcrypt

clientes = []
codigos_temporales = []

class Cliente:
    def __init__(self, id, nombres, correo, password_hash):
        self.id = id
        self.nombres = nombres
        self.correo = correo
        self.password_hash = password_hash

    @staticmethod
    def buscar_por_correo(correo):
        return next((c for c in clientes if c.correo == correo), None)

    def verificar_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)
