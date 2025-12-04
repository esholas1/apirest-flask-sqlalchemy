from flask import Flask
from flask_cors import CORS
from controllers import cliente_bp
from database import db

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clientes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(cliente_bp, url_prefix="/api/cliente")

if __name__ == "__main__":
    app.run(debug=True)
