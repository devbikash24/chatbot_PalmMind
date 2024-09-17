from flask import Flask
# from config import Config
from src.routes.upload_routes import upload_bp
from src.routes.form_routes import form_bp
from src.routes.chat_routes import chat_bp
from src.utilities.load_configuration import LoadConfiguration

app = Flask(__name__)


app_config = LoadConfiguration()
app.secret_key = app_config.secret_key

# Register blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(form_bp)
app.register_blueprint(chat_bp)

if __name__ == '__main__':
    app.run(debug=True)
