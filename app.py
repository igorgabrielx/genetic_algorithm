from flask import Flask
from routes.api import genetic

app = Flask(__name__)

# Registro do Blueprint no app principal
app.register_blueprint(genetic, url_prefix="/api/genetic")

if __name__ == '__main__':
    app.run(debug=True)