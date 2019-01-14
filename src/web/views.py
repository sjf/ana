from flask import Blueprint, session, render_template
from flask_socketio import SocketIO, emit
from random import randint

#from web import app, socketio
from web.state import *
from web.db import Db
import config, lib
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
  # Check if client is already in active game
  game_state = db.get_client_game(client_id)
  if game_state:
    log('Client in game ', game_state.id)
    if game_state and game_state.end_time > lib.now():
      return game_state

  # Try to add to the client to the most recently started game
  minimum_end_time = lib.now() + config.MIN_TIME_LEFT_MS
  game_state = db.get_latest_game(minimum_end_time)
  if game_state: log('Add client to existing game', game_state.id)
  if not game_state:
    # Start a new game for the client
    game_state = new_game()

  log('Adding client to new game ', game_state.id)
  db.set_client_game(client_id, game_state)
  return game_state

def get_client_id():
  if 'client_id' in session:
    return session['client_id']
  else:
    client_id = 'client-' + uid()
    session['client_id'] = client_id
    return client_id

words = load_word_list(config.WORD_LIST)
keys = list(words.keys())
db = Db(config.REDIS_HOST, config.REDIS_PORT)
#redis_db.flushall() # reset database during development
bp = Blueprint('views', __name__, url_prefix='')

@bp.route('/')
def index():
  game = get_game(get_client_id())
  return render_template('index.html', game=game)


# @socketio.on('submit')
# def test_message(message):
#   log('Client submitted',get_client_id(), message)
#   emit('my response', {'foo': 'bar'})

# # @socketio.on('my broadcast event', namespace='/test')
# # def test_message(message):
# #     emit('my response', {'data': message['data']}, broadcast=True)

# @socketio.on('connect')
# def on_connect(data):
#   #game_id = data['']
#   #flask_socketio.join_room();
#   #emit('my response', {'data': 'Connected'})
#   #so
#   log('Client connected',get_client_id(),data )

# @socketio.on('disconnect')
# def on_disconnect(data):
#   flask_socketio.leave_room();
#   log('Client disconnected', get_client_id(),data)
