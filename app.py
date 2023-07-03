import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


if not os.path.exists(Config.STORAGE_PATH):
    os.mkdir(Config.STORAGE_PATH)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from procompliance_test.api import api_blueprint
from procompliance_test.ui import ui_blueprint

app.register_blueprint(api_blueprint)
app.register_blueprint(ui_blueprint)

with app.app_context():
    db.create_all()
