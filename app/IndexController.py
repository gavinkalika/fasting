import flask
from flask import Flask, render_template
# from src.repository.FastSaver import FastSaver
# from src.repository.FastLoader import FastLoader
from pprint import pprint
from mysql.connector import connect


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    app.config.from_json('../var/fast-instance/config.json', silent=False)

    def get_db_conn():
        # extract into separate class
        return connect(
            host=app.config.get('DB_HOST'),
            user=app.config.get('DB_USER'),
            password=app.config.get('DB_PASSWORD'),
            database=app.config.get('DB_NAME')
        )

    @app.route('/', methods=['GET'])
    def run():
        """[summary]

        Returns:
            [type]: [description]
        """
        return render_template('index.html')

    @app.route('/register', methods=['GET'])
    def register():
        """[summary]

        Returns:
            [type]: [description]
        """
        return render_template('register.html')

    @app.route('/history', methods=['GET'])
    def history():
        """[summary]

        Returns:
            [type]: [description]
        """
        return render_template('history.html')

    @app.route('/timer', methods=['GET'])
    def timer():
        """[summary]

        Returns:
            [type]: [description]
        """
        return render_template('timer.html')

    @app.route('/login', methods=['GET'])
    def login():
        """[summary]

        Returns:
            [type]: [description]
        """
        return render_template('login.html')

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

    # @app.route('/history/all', methods=['GET'])
    # def history():
    #     loader = FastLoader(get_db_conn())
    #     # pprint(app.jinja_env)
    #     return render_template('index.html', fasts=tuple(loader.load_all()))

    return app
