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

@app.route('/', methods=['POST'])
def create():
  if not session.get('logged_in'):
    abort(401)
  g.db.execut('INSERT INTO entries(title, text) VALUES (?, ?)',
    [request.form['title'], request.form['text']])
  g.db.commit()
  flash('Created entry')
  return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config(['USERNAME'])
      error = 'Invalid username'
    elif request.form['password'] != app.config(['PASSWORD'])
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('Successfully logged in')
      return redirect(url_for('index'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('Successfully logged out')
  return redirect(url_for('index'))
if __name__ == '__main__':
  app.run()