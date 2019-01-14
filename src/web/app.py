from flask import Flask, session, render_template
from random import randint
import redis
import lib

from state import *

WORD_LIST='../data/subwords.txt'
REDIS='localhost:6379'
TIME_LIMIT_MS = 180 * 1000 # 3 minutes
FLASK_SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'


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

def get_game(client_id):
  game_id = redis_db.get(client_id)
  if game_id:
    game_state = GameState.deserialize(redis_db.get(game_id))
    log('Client in game ', game_id)
    if game_state and game_state.end_time > now():
      return game_state
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
words = load_word_list(WORD_LIST)
keys = list(words.keys())
redis_db = redis.from_url(REDIS)

@app.route('/')
def index():
  game = get_game(get_client_id())
  return render_template('index.html', game=game)
