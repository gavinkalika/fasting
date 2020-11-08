from flask import Flask
from datetime import datetime, timezone
import mysql.connector
import yaml
from src.repository.FastSaver import FastSaver

app = Flask(__name__)


@app.route('/')
def run():
    start_fast()
    return 'Hello, World!'


@app.route('/start-fast')
def start_fast():
    saver = FastSaver()
    saver.save()

