from flask import Blueprint, session, render_template
from flask_socketio import SocketIO
import flask_socketio
from random import randint 
import json

import config, lib
from . import socketio
from web.state import *
from web.db import Db
from lib import log

def load_word_list(f):
  lines = lib.readlines(f)
  subwords = {}
  for line in lines:
    w,rest = line.split(':')
    subs = rest.split(',')
    subwords[w] = subs
  return subwords

def pick_word(words, keys):
  word = keys[randint(0, len(keys))]
  return word, words[word]

def new_game():
  word, subs = pick_word(words, keys)
  time = lib.now()
  game_state = GameState(time, time + config.TIME_LIMIT_MS, word, subs)
  db.put(game_state)
  return game_state

def get_game(client_id):
  return db.get_client_game(client_id)

def get_game_for_client(client_id):
  # Check if client is already in active game
  game_state = db.get_client_game(client_id)
  if game_state:
    #log('Client in game', game_state.id)
    if game_state and game_state.end_time > lib.now():
      if client_id in game_state.client_states:
        client = game_state.client_states[client_id]
      else:
        client = ClientState(client_id)
        db.update_client_state(game_state.id, client)
      return game_state, client

  # Try to add to the client to the most recently started game
  minimum_end_time = lib.now() + config.MIN_TIME_LEFT_MS
  game_state = db.get_latest_game(minimum_end_time)
  if game_state: 
    log('Add client to existing game', game_state.id)
  else:
    # Start a new game for the client
    game_state = new_game()

  log('Adding client to new game ', game_state.id)
  db.set_client_game(client_id, game_state)
  client = ClientState(client_id)
  db.update_client_state(game_state.id, client)
  return game_state, client

def get_client_id():
  if 'client_id' in session:
    return session['client_id']
  else:
    client_id =  Key.ClientKey()
    session['client_id'] = client_id
    return client_id

def update_client_state(client_id, data):
  db.update_client_state(client_id, data['game_id'], data['subs'])

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

words = load_word_list(config.WORD_LIST)
keys = list(words.keys())
db = Db(config.REDIS_HOST, config.REDIS_PORT)
#redis_db.flushall() # reset database during development
bp = Blueprint('views', __name__)

@bp.route('/')
def index():
  game, client = get_game_for_client(get_client_id())
  return render_template('index.html', game=game, client=client)

@socketio.on('submit')
def on_submit(json_data):
  log('SOCKETIO submit',get_client_id())
  game_id, client_state = client_state_from_json(get_client_id(), json_data)
  log('Client submitted', client_state, game_id)
  db.update_client_state(game_id, client_state)

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
