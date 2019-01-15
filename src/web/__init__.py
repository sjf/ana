from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)
    app.config.from_object('config')

    from .views import bp as blueprint
    app.register_blueprint(blueprint)

    socketio.init_app(app)
    return app
