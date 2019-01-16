import pickle
from web.key import *
from lib import now 

class GameState:
  def __init__(self, start_time, end_time, word, subs):
    self.id = Key.GameKey(end_time, word)
    self.start_time = start_time
    self.end_time = end_time
    self.word = word
    self.subs = subs
    self.client_states = {}

  def serialize(self):
    return pickle.dumps(self)
  @staticmethod
  def deserialize(obj):
    return pickle.loads(obj)

  def update_client_state(self, new_client):
    if not new_client.id in self.client_states:
      self.client_states[new_client.id] = new_client
    else:
      client = self.client_states[new_client.id]
      client.update(new_client)

  def has_client(self, client_id):
    return client_id in self.client_states

  def client(self, client_id):
    return self.client_states[client_id]

  def remaining_secs(self):
    return (self.end_time - now()) // 1000

  def __repr__(self):
    return 'GameState' + repr(self.__dict__)

  def __eq__(self, other):
    if type(self) != type(other):
      return False
    return self.__dict__ == other.__dict__

class ClientState:
  def __init__(self, id_, accepted=[], rejected=[]):
    self.id = id_
    self.accepted = accepted[:]
    self.rejected = rejected[:]

  def serialize(self):
    return pickle.dumps(self)
  @staticmethod
  def deserialize(obj):
    return pickle.loads(obj)

  def __repr__(self):
    return 'ClientState' + repr(self.__dict__)

  def __eq__(self, other):
    if type(self) != type(other):
      return False
    return self.__dict__ == other.__dict__

  def update(self, other):
    update(self.accepted, other.accepted)
    update(self.rejected, other.rejected)

def update(l1, l2):
  for x in l2:
    if x not in l1:
      l1.append(x)
