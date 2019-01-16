from flask import Blueprint, session, render_template
from flask_socketio import SocketIO
import flask_socketio
import json

import config, lib
from . import socketio
from web.state import *
from web.db import Db
from web.game import Game
from lib import log

def get_client_id():
  if 'client_id' in session:
    return session['client_id']
  else:
    client_id =  Key.ClientKey()
    session['client_id'] = client_id
    return client_id

def valid_word(w):
  if not w:
    return false
  # TODO only accept ascii text
  return w

def client_state_from_json(client_id, json_data):
  # TODO use a proper schema
  data = json.loads(json_data)
  if not data:
    return None, None
  if 'game_id' not in data:
    return None, None
  if 'accepted' not in data or type(data['accepted']) != type([]):
    return None, None
  if 'rejected' not in data or type(data['rejected']) != type([]):
    return None, None
  # Filter empty strings
  accepted = list(filter(valid_word, data['accepted']))
  rejected = list(filter(valid_word, data['rejected']))
  client = ClientState(client_id, accepted, rejected)
  return data['game_id'], client

db = Db(config.REDIS_HOST, config.REDIS_PORT)
game = Game.new(db)
#redis_db.flushall() # reset database during development
bp = Blueprint('views', __name__)

@bp.route('/')
def index():
  game_state, client = game.get_game_for_client(get_client_id())
  return render_template('index.html', game=game_state, client=client)

@socketio.on('submit')
def on_submit(json_data):
  log('SOCKETIO submit',get_client_id())
  game_id, client_state = client_state_from_json(get_client_id(), json_data)
  log('Client submitted', client_state, game_id)
  #db.update_client_state(game_id, client_state)

# @socketio.on('my broadcast event', namespace='/test')
# def test_message(message):
#     emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect')
def on_connect():
  log('SOCKETIO Connected',get_client_id())
  # client_id = get_client_id()
  # game = get_game(client_id)
  # if not game: 
  #   log("Client not in game")
  #   return
  # # Add client to room for the game they are in
  # flask_socketio.join_room(game.id);
  # log('Client connected', client_id)

@socketio.on('disconnect')
def on_disconnect():
  log('SOCKETIO disconnected',get_client_id())
  # Clients are automatically removed from any rooms they are in
