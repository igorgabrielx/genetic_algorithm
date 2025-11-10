from flask import Flask
from routes.api import genetic
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Registro do Blueprint no app principal
app.register_blueprint(genetic, url_prefix="/api/genetic")

if __name__ == '__main__':
    app.run(debug=True)