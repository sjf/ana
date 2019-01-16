import pytest
import redis
import testing.redis

from web.db import Db
from web.db import Key
from web.tests.test_common import *

@pytest.fixture
def redis_db():
  redis = testing.redis.RedisServer()
  redis.start()
  yield redis
  redis.stop()

def new(redis_db):
  return Db(redis_db.dsn()['host'], redis_db.dsn()['port'])


def test_put_get_game(redis_db):
  db = new(redis_db)

  g = game()
  db.put(g)

  assert g == db.get_game(g.id)

def test_set_and_get_client_game(redis_db):
  db = new(redis_db)

  id_ = 'client-1234'
  g = game()
  db.put(g)
  assert db.get_client_game(id_) == None

  db.set_client_game(id_, g)
  assert g == db.get_client_game(id_)

def test_get_latest_game(redis_db):
  db = new(redis_db)
  assert None == db.get_latest_game(9999)

  g1 = game(1234)
  db.put(g1)
  g2 = game(4567)
  db.put(g2)
  g3 = game(7890)
  db.put(g3)
  
  assert None == db.get_latest_game(7891)
  assert g3 == db.get_latest_game(7889)

def test_update_client_state(redis_db):
  db = new(redis_db)
  g = game()
  g.client_states = {}
  db.put(g)

  c = client()
  db.update_client_state('game-does-not-exist', c)
  # Game does not exist, db not updated
  assert None == db.get_game('game-does-not-exist')

  db.update_client_state(g.id, c)
  g2 = db.get_game(g.id)
  # Client not in game, game not updated
  assert c.id not in g2.client_states

  db.set_client_game(c.id, g)
  db.update_client_state(g.id, c)
  g2 = db.get_game(g.id)
  assert c == g2.client_states[c.id]

  c.accepted.extend(['a','b'])
  c.rejected.extend(['x','y'])
  db.update_client_state(g.id, c)
  g2 = db.get_game(g.id)
  assert c == g2.client_states[c.id]


