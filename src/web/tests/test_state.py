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