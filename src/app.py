#!/usr/bin/env python

import os
import json
import random
import redis
import logging
from flask import Flask, jsonify, render_template, redirect, url_for, request
import flask_login

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

port = os.getenv('PORT', 3000)
debug = os.getenv('DEBUG', False)
redis_host = os.getenv('REDIS_HOST', 'redis')

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
r = redis.Redis(host=redis_host, port=6379, db=0, charset="utf-8", decode_responses=True)

class User(flask_login.UserMixin):
    pass

def get_players():
    try:
        players = r.lrange('players', 0, -1)
        logger.info(players)
    except:
        players = []
        logger.info("no users")
    return players

def add_user(username):
    r.rpush('players', username)

@login_manager.user_loader
def user_loader(username):
    users = get_players()
    logger.info(users)
    if username not in users:
      #add_user(username)
      return

    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    logger.info(username)
    users = get_players()

    if username not in users:
      return

    user = User()
    user.id = username
    return user

@app.route('/healthz', methods=['GET'])
def healthz():
  return jsonify({'status':'ok'}), 200, {'ContentType':'application/json'}

@app.route('/kitty', methods=['GET'])
@flask_login.login_required
def kitty():
  current_user = flask_login.current_user.id
  r.lpush('logged_in', current_user)
  drawing = False
  try:
    winner_name = r.lrange('winner', 0, 0)
    if len(winner_name) > 0:
      drawing = True
  except:
     drawing = False

  if drawing:
    return render_template('kitty', current_user=current_user)
  else:
    return render_template('waiting', current_user=current_user)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index')

    if request.method == 'POST':
        user = User()
        user.id = request.form['username'].lower()
        flask_login.login_user(user)
        return redirect(url_for('kitty'))

    return 'Bad Login'

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@app.route('/results', methods=['GET'])
@flask_login.login_required
def results():
  current_user = flask_login.current_user.id
  winner = False
  winner_name = ""
  try:
      winner_name = r.lrange('winner', 0, 0)
      if winner_name[0].lower() == current_user.lower():
          winner = True
  except:
    return render_template('waiting', current_user=current_user)
  return render_template('results', current_user=current_user, winner=winner, winner_name=winner_name[0])

@app.route('/drawing', methods=['GET'])
@flask_login.login_required
def drawing():
  players = get_players()
  winner = random.choice(players)
  logger.info(f"Good Luck Kitty Winner: {winner}")
  r.lpush('winner', winner)
  return jsonify({'winner':winner}), 200, {'ContentType':'application/json'}

@app.route('/winner', methods=['GET'])
@flask_login.login_required
def winner():
  winner = r.lrange('winner', 0, 0)
  return jsonify({'winner':winner}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=port, debug=debug)
