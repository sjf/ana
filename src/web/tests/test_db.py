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

def test_put_get_game(redis_db):
  db = Db(redis_db.dsn()['host'], redis_db.dsn()['port'])

  g = game()
  db.put(g)

  assert g == db.get_game(g.id)

def test_get_client_game(redis_db):
  db = Db(redis_db.dsn()['host'], redis_db.dsn()['port'])

  id_ = 'client-1234'
  g = game()
  db.put(g)
  assert db.get_client_game(id_) == None

  db.set_client_game(id_, g)
  assert g == db.get_client_game(id_)

def test_get_latest_game(redis_db):
  db = Db(redis_db.dsn()['host'], redis_db.dsn()['port'])
  assert None == db.get_latest_game(9999)

  g1 = game(1234)
  db.put(g1)
  g2 = game(4567)
  db.put(g2)
  g3 = game(7890)
  db.put(g3)
  
  assert None == db.get_latest_game(7891)
  assert g3 == db.get_latest_game(7889)
