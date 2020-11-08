from flask import Flask
from src.repository.FastSaver import FastSaver

app = Flask(__name__)


@app.route('/')
def run():
    return 'Hello, World!'


@app.route('/start-fast')
def start_fast():
    saver = FastSaver()
    saver.start_fast()

@app.route('/end-fast')
def end_fast():
    saver = FastSaver()
    saver.end_fast()
