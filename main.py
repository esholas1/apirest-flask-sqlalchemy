from flask import Flask
from flask_cors import CORS
from controllers import cliente_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(cliente_bp, url_prefix="/api/cliente")

if __name__ == "__main__":
    app.run(debug=True)
