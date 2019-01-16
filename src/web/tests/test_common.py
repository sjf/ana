from web.state import *

def client(id_='client-1234', accepted = ['asdf123', 'asdf456'], rejected = ['bbb123', 'bbb456']):
  return ClientState(id_, accepted, rejected)

def game(endtime=1234):
  c1 = client('client-111')
  c2 = client('client-222')
  g = GameState(1, endtime, 'foo', ['ab','bc'])
  g.update_client_state(c1)
  g.update_client_state(c2)
  return g
