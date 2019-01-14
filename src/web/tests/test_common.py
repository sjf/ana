from web.state import *

def client(n=1234):
  c = ClientState('client-' + str(n))
  c.accepted.append('asdf123')
  c.accepted.append('asdf456')
  c.rejected.append('bbb123')
  c.rejected.append('bbb456')
  return c

def game(endtime=1234):
  c1 = client(111)
  c2 = client(222)
  g = GameState(1, endtime, 'foo', ['ab','bc'])
  g.update_client_state(c1)
  g.update_client_state(c2)
  return g
