from database import db
import bcrypt

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @staticmethod
    def buscar_por_correo(correo):
        return Cliente.query.filter_by(correo=correo).first()

    def verificar_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)
