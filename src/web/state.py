import pickle
from lib import *

class GameState:
  def __init__(self, start_time, end_time, word, subs):
    self.id = 'game-' + uid() + '-' + word
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

  def update_client_state(self, client):
    self.client_states[client.id] = client

  def remaining_secs(self):
    log('start:', self.start_time)
    log('end:  ', self.end_time)
    log('now:  ', now())
    return (self.end_time - now()) // 1000

  def __repr__(self):
    return 'GameState' + repr(self.__dict__)

  def __eq__(self, other):
    if type(self) != type(other):
      return False
    return self.__dict__ == other.__dict__

class ClientState:
  def __init__(self, id_):
    self.id = 'client-' + id_
    self.accepted = []
    self.rejected = []

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
