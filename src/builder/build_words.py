#!/usr/bin/env python3
from collections import defaultdict
from itertools import combinations
import sys
import lib

DICT="dict.txt" if len(sys.argv) < 2 else sys.argv[1]
DB="subwords.txt" if len(sys.argv) < 3 else sys.argv[2]
MAX=6
MIN=3

def subsets(w):
  if not w:
    return []
  result = []
  for i in range(1, len(w)):
    subs = map(lib.joinstr, combinations(w,i))
    result.extend(subs)
  result.append(w)
  return result

def filter_(words):
  words = filter(lambda w:not w[0].isupper(), words)
  words = filter(lambda w:'-' not in w, words)
  if MAX:
    words = filter(lambda x:len(x) <= MAX, words)
  if MIN:
    words = filter(lambda x:len(x) >= MIN, words)
  return list(words)

def get_words(f):
  words = filter_(lib.readlines(f))
  return words

def get_subwords(words):
  anagrams = defaultdict(list)
  for w in words:
    key = lib.sortstr(w)
    anagrams[key].append(w)

  subwords = defaultdict(list)
  keys = filter(lambda x:len(x) == MAX if MAX else x, words)
  for w in keys:
    subs = subsets(w)
    for sub in subs:
      key = lib.sortstr(sub)
      subwords[w].extend(anagrams[key])
  return subwords

def output(dict_, f):
  fh = open(f,'w')
  for k,v in dict_.items():
    fh.write(k + ':' + ','.join(v) + '\n')

if __name__ == '__main__':
  words = get_words(DICT)
  subwords = get_subwords(words)
  output(subwords, DB)
