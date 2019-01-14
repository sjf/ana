from lib import uid

class Key:
  @staticmethod
  def end_time(key):
    if not key.startswith('game-') or key.count('-') < 3:
      raise Exception('Invalid game key: ' + key)
    return int(key.split('-')[1])

  @staticmethod
  def GameKey(end_time, word):
    return 'game-' + str(end_time) + '-' + uid() + '-' + word

  @staticmethod
  def ClientKey(id_):
    return 'client-' + id_