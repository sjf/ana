import redis

from web.state import *
from lib import *

def _tostr(bytes):
  """ Redis keys are returned as byte arrays even though they are supposed to be strings."""
  if bytes is None:
    return None
  return str(bytes, 'utf-8')

class Db:
  def __init__(self, host, port):
    self.redis_db = redis.StrictRedis(host=host, port=port)

  def put(self, item, pipe=None):
    if not pipe: pipe = self.redis_db

    pipe.set(item.id, item.serialize())

  def get_game(self, id_, pipe=None):
    if not pipe: pipe = self.redis_db

    if not id_.startswith('game-'):
      raise Exception('Not client key')

    val = pipe.get(id_)

    if not val:
      return None  
    return GameState.deserialize(val)

  def get_client_game(self, id_, pipe=None):
    if not pipe: pipe = self.redis_db
    if not id_.startswith('client-'):
      raise Exception('Not client key')

    game_id = _tostr(pipe.get(id_))
    if not game_id:
      return None
    return self.get_game(game_id, pipe)

  def add_client_to_game(self, game, client, pipe=None):
    assert isinstance(game, GameState)
    assert isinstance(client, ClientState)

    self.redis_db.set(client.id, game.id)
    return self.update_client_state(game.id, client)

  def set_client_game(self, id_, game, pipe=None):
    assert isinstance(game, GameState)
    if not pipe: pipe = self.redis_db

    if not id_.startswith('client-'):
      raise Exception('Not client key')
    pipe.set(id_, game.id)

  def get_latest_game(self, minimum_end_time, pipe=None):
    if not pipe: pipe = self.redis_db

    mx = '' # Get the key with largest time stamp
    for key in pipe.scan_iter('game-*'):
      mx = max(_tostr(key), mx)
    if not mx:
      return None
    end_time = Key.end_time(mx)
    if end_time > minimum_end_time: 
      return self.get_game(mx, pipe)
    return None

  def update_client_state(self, game_id, client_state):
    game_state = None
    def _update_client_state(pipe):
      nonlocal game_state
      game_state = self.get_client_game(client_state.id, pipe)
      if not game_state or game_state.id != game_id:
        log('Incorrect game id for client', client_state.id, game_id);
        game_state = None # return value
        return
      game_state.update_client_state(client_state)
      self.put(game_state, pipe)
    try:
      self.redis_db.transaction(_update_client_state)
      return game_state
    except redis.WatchError as e:
      log(e)
      return None

