import flask
from flask import Flask, render_template
from src.repository.FastSaver import FastSaver
from src.repository.FastLoader import FastLoader
from pprint import pprint
import mysql.connector


def create_app(test_config=None):
    # create and configure the app
    app = Flask('fast', instance_relative_config=True, root_path="../src/")

    app.config.from_json('config.json', silent=False)

    def get_db_conn():
        # extract into separate class
        return mysql.connector.connect(
            host=app.config.get('DB_HOST'),
            user=app.config.get('DB_USER'),
            password=app.config.get('DB_PASSWORD'),
            database=app.config.get('DB_NAME')
        )

    @app.route('/', methods=['GET'])
    def run():
        return 'Hello World'

    @app.route('/start-fast', methods=['POST'])
    def start_fast():
        saver = FastSaver(get_db_conn())
        saver.start_fast()
        return flask.Response(status=200)

    @app.route('/end-fast', methods=['POST'])
    def end_fast():
        saver = FastSaver(get_db_conn())
        saver.end_fast()
        return flask.Response(status=200)

    @app.route('/history/all', methods=['GET'])
    def history():
        loader = FastLoader(get_db_conn())
        # pprint(app.jinja_env)
        return render_template('index.html', fasts=tuple(loader.load_all()))

    return app
