def joinstr(l):
  return "".join(l)

def sortstr(w):
  return joinstr(sorted(w))

def readlines(f):
  """ Returns the non-empty lines from f, with whitespace stripped."""
  lines = open(f).readlines()
  lines = filter(lambda x:x, map(lambda x:x.strip(), lines))
  return lines
