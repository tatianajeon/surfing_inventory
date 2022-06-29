from flask import Flask
from.site.routes import site
from config import Config
from .authentication.routes import auth

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db as root_db


app = Flask(__name__)
app.register_blueprint(site)
app.register_blueprint(auth) 


app.config.from_object(Config)

root_db.init_app(app)

migrate= Migrate(app, root_db)