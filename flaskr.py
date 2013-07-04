#!/usr/bin/python
import sqlite3
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
  
if __name__ == '__main__':
  app.run()