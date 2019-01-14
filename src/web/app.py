from flask import Flask, session, render_template
from flask_socketio import SocketIO, emit
from random import randint
import redis
import lib

from state import *

WORD_LIST='../data/subwords.txt'
REDIS='localhost:6379'
TIME_LIMIT_MS = 600*1000 #180 * 1000 # 3 minutes
MIN_TIME_LEFT_MS = 20*1000 #Only add clients to a game with more than this time left
FLASK_SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/' # should be secret

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
  time = now()
  game_state = GameState(time, time + TIME_LIMIT_MS, word, subs)
  redis_db.set(game_state.id, game_state.serialize())
  return game_state

def load_game(game_id):
  return GameState.deserialize(redis_db.get(game_id))

def get_latest_game():
  mx = b'' # Get the key with largest time stamp
  for key in redis_db.scan_iter('game-*'):
    mx = max(key, mx)
  if not mx:
    return None
  end_time = GameState.end_time(mx)
  if end_time - now() > MIN_TIME_LEFT_MS: # More than 20s left in game
    return load_game(mx)
  return None

def get_game(client_id):
  # Check if client is already in active game
  game_id = redis_db.get(client_id)
  if game_id:
    game_state = load_game(game_id)
    log('Client in game ', game_id)
    if game_state and game_state.end_time > now():
      return game_state

  # Try to add to the client to the most recently started game
  game_state = get_latest_game()
  if game_state: log('Add client to existing game', game_state.id)
  if not game_state:
    # Start a new game for the client
    game_state = new_game()

  log('Adding client to new game ', game_state.id)
  redis_db.set(client_id, game_state.id)
  return game_state

def get_client_id():
  if 'client_id' in session:
    return session['client_id']
  else:
    client_id = 'client-' + uid()
    session['client_id'] = client_id
    return client_id

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
socketio = SocketIO(app)

words = load_word_list(WORD_LIST)
keys = list(words.keys())
redis_db = redis.from_url(REDIS)
#redis_db.flushall() # reset database during development

@app.route('/')
def index():
  game = get_game(get_client_id())
  return render_template('index.html', game=game)

@socketio.on('submit')
def test_message(message):
  log('Client submitted',get_client_id(), message)
  emit('my response', {'foo': 'bar'})

# @socketio.on('my broadcast event', namespace='/test')
# def test_message(message):
#     emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect')
def test_connect():
  emit('my response', {'data': 'Connected'})
  log('Client connected',get_client_id() )

@socketio.on('disconnect')
def test_disconnect():
  log('Client disconnected', get_client_id())
