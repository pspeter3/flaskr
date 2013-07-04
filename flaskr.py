#!/usr/bin/python
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
  render_template, flash

# Config
DATABASE = 'db/flaskr.db'
DEBUG = True
SECRET_KEY = 'flaskr-python'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
  cursor = g.db.execute('SELECT title, text FROM entries ORDER BY id DESC')
  entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
  return render_template('index.html', entries=entries)

if __name__ == '__main__':
  app.run()