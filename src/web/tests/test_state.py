import pytest
from web.state import *
from web.key import *
from web.tests.test_common import *

def test_game_state_serialization():
  g = game()
  s=g.serialize()
  g2=GameState.deserialize(s)

  assert g == g2
  assert g2.id.startswith('game-')
  assert g.end_time == Key.end_time(g2.id)

def test_client_state_serialization():
  c = client()
  s=c.serialize()
  c2=ClientState.deserialize(s)

  assert c == c2
  assert c2.id.startswith('client-')

def test_update_client():
  c = client(1, ['b','c'], [])
  c2 = client(2, ['a','b','c'], ['d','e'])

  c.update(c2)
  assert c.accepted == ['b','c','a']
  assert c.rejected == ['d','e']

def test_game_update_client():
  g = game()
  c = client('client-1', ['a'], ['x'])
  assert c.id not in g.client_states

  g.update_client_state(c)
  assert g.client_states[c.id] == c

  c2 = client('client-1', ['a', 'b', 'c'], ['x', 'y', 'z'])
  assert g.client_states[c.id] != c2
  g.update_client_state(c2)
  assert g.client_states[c.id] == c2
