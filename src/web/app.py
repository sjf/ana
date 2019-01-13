from flask import Flask
from flask import render_template
from random import randint

import lib
DB='../data/subwords.txt'

def load(f):
  lines = lib.readlines(f)
  subwords = {}
  for line in lines:
    w,rest = line.split(':')
    subs = rest.split(',')
    subwords[w] = subs
  return subwords

def pick(db, keys):
  word = keys[randint(0, len(keys))]
  return word, db[word]

app = Flask(__name__)
db = load(DB)
keys = list(db.keys())

@app.route('/')
def hello_world():
  word, subs = pick(db, keys)
  return render_template('index.html', word=word, subs=subs)
