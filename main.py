from flask import Flask, request
from flask_socketio import SocketIO, send, emit
from functions import *
from globals import *
from classes import *


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("connect")
def on_connect():
    print("Client connected")


@socketio.on("root")
def on_root(*msg):
    print("Root message received:", msg)
    emit("root", {"serverVersion": SERVER_VERSION})


@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected")


@app.route("/", methods=["GET"])
def index():
    return {"serverVersion": SERVER_VERSION}, 200


@app.route("/session/create", methods=["POST"])
def create_session():
    # get a new unique session id
    new_session_id: int or None = get_new_id(sessions, IdType.SESSION)

    # if the maximum number of sessions has been reached
    if new_session_id == None:
        return {"msg": "Maximum number of sessions reached."}, 400

    # create a new session
    session = Session(id=new_session_id)
    sessions.append(session)

    return {"sessionId": session.id}, 201


@app.route("/session/join/<int:session_id>", methods=["POST"])
def join_session(session_id: int):
    # if the session does not exist
    if not session_exists(session_id, sessions):
        return {"msg": "Session does not exist."}, 404

    # if the session is full
    if session_is_full(session_id, sessions):
        return {"msg": "Session is full."}, 503

    # get the user's nickname
    nickname: str or None = request.form.get("nickname")

    # if the nickname is not provided
    if nickname == None:
        return {"msg": "Nickname not provided."}, 400

    # get the session
    session: Session = get_session(session_id=session_id, sessions=sessions)

    # create a new player
    player: Player = Player(
        id=get_new_id(
            session.all_players(), IdType.PLAYER,
        ),
        nickname=nickname,
    )

    # add the player to the session
    session.unassigned_players.append(player)

    # notify all players in the session that a new player has joined
    emit(
        "player_joined",
        {
            "player": player.to_dict()
        },
        room=session.id,
    )

    return {"playerId": player.id}, 201


if __name__ == '__main__':
    socketio.run(app, port=PORT, host="0.0.0.0", debug=DEBUG)
