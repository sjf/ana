TIME_LIMIT = 180
import pickle

class GameState:
  def __init__(self, id_, start_time, time_limit, word, subs):
    self.id = id_
    self.start_time = start_time
    self.end_time = start_time + time_limit
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

  def __repr__(self):
    return 'GameState' + repr(self.__dict__)

  def __eq__(self, other):
    if type(self) != type(other):
      return False
    return self.__dict__ == other.__dict__

class ClientState:
  def __init__(self, id_):
    self.id = id_
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
