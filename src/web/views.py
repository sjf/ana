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
import jsonschema

def get_client_id():
  """ Returns the client ID from the Flask session which is stored in an 
      encrypted cookie. Generates and stores new ID if one is not found."""
  if 'client_id' in session:
    return session['client_id']
  else:
    client_id =  Key.ClientKey()
    session['client_id'] = client_id
    return client_id

def generate_username(client_id):
  hsh = hash(client_id)
  n_adj = len(config.ADJECTIVES)
  n_nouns = len(config.NOUNS)
  return config.ADJECTIVES[hsh % n_adj] + "_" + config.NOUNS[hsh % n_nouns]

def is_valid_submission(json_data):
  try:
    #jsonschema.validate(json_data, config.SUBMIT_SCHEMA)
    return True
  except jsonschema.ValidationError as e:
    log("Invalid client response:",e,json_data)
    return False

def valid_word(w):
  if not w:
    return false
  # TODO only accept ascii text
  return w

def client_state_from_json(client_id, json_data):
  # TODO use a proper schema
  data = json.loads(json_data)
  if not is_valid_submission(json_data):
    return
  accepted = list(filter(valid_word, data['accepted']))
  rejected = list(filter(valid_word, data['rejected']))
  client = ClientState(client_id, accepted, rejected)
  return data['game_id'], client

def get_score(words):
  score = 0
  for word in words:
    score += len(words)
  score *= 10
  return score

def get_other_players_scores(client_id, game_state):
  result = []
  for client in game_state.client_states.values():
    if client.id == client_id: continue
    result.append({'client_id': generate_username(client.id),
                   'score': get_score(client.accepted)})
  return result

db = Db(config.REDIS_HOST, config.REDIS_PORT)
game = Game.new(db)
#redis_db.flushall() # reset database during development
bp = Blueprint('views', __name__)

@bp.route('/')
def index():
  game_state, client = game.get_game_for_client(get_client_id())
  others = get_other_players_scores(client.id, game_state)
  return render_template('index.html', game=game_state, client=client, other_players_scores=others)

@socketio.on('submit')
def on_submit(json_data):
  log('SOCKETIO submit',get_client_id())
  game_id, client_state = client_state_from_json(get_client_id(), json_data)
  log('Client submitted', client_state, game_id)
  game.update_client_from_submit(game_id, client_state)

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
