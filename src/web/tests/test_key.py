from web.key import *

def test_key():
  c = Key.ClientKey('asdf')
  assert c.startswith('client-')

  g = Key.GameKey(1234, 'foo')
  assert g.startswith('game-')
  assert g.split('-').count('1234') == 1
  assert g.split('-').count('foo') == 1