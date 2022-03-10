from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = "ClaveSecreta"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/sesionesFlaskORM"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)


from .sesiones import sesiones

def create_app():
    app.register_blueprint(sesiones)
    return  app
