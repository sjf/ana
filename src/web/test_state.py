import pytest
from state import *

def test_game_state_serialization():
  c = ClientState('client-1234')
  c.accepted.append('asdf123')
  c.accepted.append('asdf456')
  c.rejected.append('bbb123')
  c.rejected.append('bbb456')

  g = GameState(123, 10, 'foo', ['ab','bc'])
  g.update_client_state(c)
  s=g.serialize()
  g2=GameState.deserialize(s)

  assert g == g2
  assert g.id.startswith(b'game-')
  assert 10 == GameState.end_time(g.id)

def test_client_state_serialization():
  c = ClientState('client-1234')
  c.accepted.append('asdf123')
  c.accepted.append('asdf456')
  c.rejected.append('bbb123')
  c.rejected.append('bbb456')

  s=c.serialize()
  c2=ClientState.deserialize(s)

  assert c == c2
  assert c.id.startswith(b'client-')