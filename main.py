from socket import socket
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from cashx1.engine import Engine
from cashx1.entrada import SocketCashGamex1


engine = Engine()
app = Flask(__name__)

app.config["SECRET_KEY"] = "ADSDASDASD4234X3"
cors = CORS(app, resources={r"*": {"origins": "*"}})
socket = SocketIO(app, cors_allowed_origins="*")


@socket.on("addPlayerCashGameX1")
def on_addPlayer(data):
    SocketCashGamex1(data)


@socket.on("cartaPlayerCashGameX1")
def on_cartaPlayer(data):
    SocketCashGamex1(data)


if __name__ == "__main__":
    socket.run(app, debug=True)
