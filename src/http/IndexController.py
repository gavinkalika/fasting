import flask
from flask import Flask
from src.repository.FastSaver import FastSaver

app = Flask(__name__)


@app.route('/', methods=['GET'])
def run():
    return 'Hello, World!'


@app.route('/start-fast', methods=['POST'])
def start_fast():
    saver = FastSaver()
    saver.start_fast()
    return flask.Response(status=200)


@app.route('/end-fast', methods=['POST'])
def end_fast():
    saver = FastSaver()
    saver.end_fast()
    return flask.Response(status=200)
