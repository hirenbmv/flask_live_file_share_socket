from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

socketio = SocketIO()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from app.configurations.config import Developement
    app.config.from_object(Developement)

    socketio.init_app(app)
    db.init_app(app)

    from app.views.views import views_blueprint
    app.register_blueprint(views_blueprint)

    return app
