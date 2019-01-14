import uuid
import time

def joinstr(l):
  return "".join(l)

def sortstr(w):
  return joinstr(sorted(w))

def readlines(f):
  """ Returns the non-empty lines from f, with whitespace stripped."""
  lines = open(f).readlines()
  lines = filter(lambda x:x, map(lambda x:x.strip(), lines))
  return lines

def now():
  """ Return the current timestamp in milliseconds. """
  return int(round(time.time() * 1000))

def log(*strs):
  print(*strs)

def uid():
  return uuid.uuid4().hex