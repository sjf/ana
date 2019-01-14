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

  def put(self, item):
    self.redis_db.set(item.id, item.serialize())

  def get_game(self, id_):
    if not id_.startswith('game-'):
      raise Exception('Not client key')
    val = self.redis_db.get(id_)
    if not val:
      return None  
    return GameState.deserialize(val)

  def get_client_game(self, id_):
    if not id_.startswith('client-'):
      raise Exception('Not client key')
    game_id = _tostr(self.redis_db.get(id_))
    if not game_id:
      return None
    return self.get_game(game_id)

  def set_client_game(self, id_, game):
    if not id_.startswith('client-'):
      raise Exception('Not client key')
    self.redis_db.set(id_, game.id)

  def get_latest_game(self, minimum_end_time):
    mx = '' # Get the key with largest time stamp
    for key in self.redis_db.scan_iter('game-*'):
      mx = max(_tostr(key), mx)
    if not mx:
      return None
    end_time = Key.end_time(mx)
    if end_time > minimum_end_time: 
      return self.get_game(mx)
    return None

