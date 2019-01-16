import pytest
import redis
import testing.redis

from web.game import Game
from web.db import Db
from web.db import Key
from web.tests import test_common 

@pytest.fixture
def redis_db():
  redis = testing.redis.RedisServer()
  redis.start()
  yield redis
  redis.stop()

WORDS = {'ear':['era','are'],
         'one':['one','eon'],
         'bar':['bra']}

def new(redis_db):
  db = Db(redis_db.dsn()['host'], redis_db.dsn()['port'])
  return Game(db, WORDS),db

def test_new_game(redis_db):
  gm, db = new(redis_db)
  g = gm._new_game()
  assert db.get_game(g.id) == g

def test_get_game_for_client_new_client(redis_db):
  gm, db = new(redis_db)
  id_ = 'client-1234'
  game_state, client = gm.get_game_for_client(id_)
  assert client.id == id_
  assert game_state.has_client(id_)
  assert client == game_state.client(id_)
  assert gm.get_game(id_) == game_state

def test_get_game_for_client_client_in_existing_game(redis_db):
  gm, db = new(redis_db)
  id_ = 'client-1234'
  game1 = gm._new_game()
  c = test_common.client(id_,[],[])
  db.add_client_to_game(game1, c)

  game_state, client = gm.get_game_for_client(id_)
  assert client.id == id_
  assert game_state.id == game1.id
  assert c == game_state.client(id_)

def test_get_game_for_client_add_client_to_existing_game(redis_db):
  gm, db = new(redis_db)
  id_ = 'client-1234'
  game1 = gm._new_game()
  c = test_common.client(id_,[],[])

  game_state, client = gm.get_game_for_client(id_)
  assert client.id == id_
  assert game_state.id == game1.id
  assert c == game_state.client(id_)