from flask import Flask
from flask_socketio import SocketIO
import web.views

app = Flask(__name__)
app.config.from_object('config')
print(app.config)
app.register_blueprint(web.views.bp)
socketio = SocketIO(app)

if __name__ == '__main__':
  app.run(debug=True)