from random import randint 
import lib
import config
from web.state import *
from lib import log

class Game:
  def __init__(self, db, words) :
    self.db = db
    self.words = words
    self.keys = list(words.keys())

  @staticmethod
  def new(db):
    return Game(db, Game._load_word_list(config.WORD_LIST))

  def _new_game(self):
    word, subs = self._pick_word()
    time = lib.now()
    game_state = GameState(time, time + config.TIME_LIMIT_MS, word, subs)
    self.db.put(game_state)
    return game_state

  def get_game_for_client(self, client_id):
    # Check if client is already in active game
    game_state = self.db.get_client_game(client_id)
    if game_state:
      #log('Client in game', game_state.id)
      if game_state and game_state.end_time > lib.now():
        if game_state.has_client(client_id):
          client = game_state.client(client_id)
        else:
          client = ClientState(client_id)
          self.db.add_client_to_game(game_state, client)
        return game_state, client

    # Try to add to the client to the most recently started game
    minimum_end_time = lib.now() + config.MIN_TIME_LEFT_MS
    game_state = self.db.get_latest_game(minimum_end_time)
    if not game_state: 
      # Start a new game for the client
      game_state = self._new_game()
    else:
      log('Add client to existing game', game_state.id)

    log('Adding client to game ', game_state.id)
    client = ClientState(client_id)
    game_state = self.db.add_client_to_game(game_state, client)
    return game_state, client

  def get_game(self, client_id):
    return self.db.get_client_game(client_id)

  def _pick_word(self):
    word = self.keys[randint(0, len(self.keys)-1)]
    return word, self.words[word]

  @staticmethod
  def _load_word_list(f):
    lines = lib.readlines(f)
    subwords = {}
    for line in lines:
      w,rest = line.split(':')
      subs = rest.split(',')
      subwords[w] = subs
    return subwords
