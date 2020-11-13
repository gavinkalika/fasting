import flask
from flask import Flask
from src.repository.FastSaver import FastSaver
from src.repository.FastLoader import FastLoader
from pprint import pprint


def create_app(test_config=None):
    # create and configure the app
    app = Flask('fast', instance_relative_config=True)

    app.config.from_json('config.json', silent=True)

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

    @app.route('/history/all', methods=['GET'])
    def history():
        loader = FastLoader()
        return loader.load_all()

    return app
