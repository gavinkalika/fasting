import flask
from cerberus import Validator
from flask import Flask, render_template, request, redirect, session, flash

from app.exception.ExceedLimitException import ExceedLimitException
from app.repository.UserSaver import UserSaver
from app.repository.FastSaver import FastSaver
from app.repository.UserLoader import UserLoader
from app.repository.FastLoader import FastLoader
from pprint import pprint
from mysql.connector import connect
from validator import validate


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = 'secret'

    app.config.from_json('../var/fast-instance/config.json', silent=False)

    schema = {}
    v = Validator(schema)

    def get_db_conn():
        # extract into separate class
        return connect(
            host=app.config.get('DB_HOST'),
            user=app.config.get('DB_USER'),
            password=app.config.get('DB_PASSWORD'),
            database=app.config.get('DB_NAME')
        )

    def auth_check() -> str:
        val = session.get("username")

        if val is None:
            flash("Unauthorized")
            return redirect('/')

        return val

    @app.route('/', methods=['GET'])
    def run():
        """[summary]

        Returns:
            [type]: [description]
        """
        if session.get("username"):
            return render_template('index_auth.html', username=session.get("username"))

        return render_template('index.html', username=session.get("username"))

    @app.route('/register', methods=['GET'])
    def register():
        """[summary]

        Returns:
            [type]: [description]
        """
        return render_template('register.html')

    @app.route('/register-save', methods=['POST'])
    def register_save():
        """Saves data from register form.

        Returns:
            [type]: [description]
        """

        req = request.form
        saver = UserSaver(get_db_conn())

        # need to validate data
        data_to_validate = {
            "email": req.get('email'),
            "password": req.get('password')
        }

        rules = {"email": "mail",
                 "password": "string|min:5"
                 }

        result, _, errors = validate(req=data_to_validate, rules=rules, return_info=True)
        if not result:
            for key in errors:
                field_name = key
                for k in errors[key]:
                    flash("{0} field {1}".format(field_name, errors[key][k].lower()))

            return redirect('/register')

        saver.save_user(email=req.get('email'), password=req.get('password'))

        session["username"] = req.get('email')

        return redirect('/')

    @app.route('/history', methods=['GET'])
    def history():
        """[summary]

        Returns:
            [type]: [description]
        """
        username = auth_check()

        return render_template('history.html', username=username)

    @app.route('/timer', methods=['GET'])
    def timer():
        """[summary]

        Returns:
            [type]: [description]
        """
        username = auth_check()
        return render_template('timer.html', username=username)

    @app.route('/login', methods=['GET'])
    def login():
        """[summary]

        Returns:
            [type]: [description]
        """
        return render_template('login.html')

    @app.route('/login-post', methods=['POST'])
    def login_post():
        """[summary]

        Returns:
            [type]: [description]
        """
        loader = UserLoader(get_db_conn())

        req = request.form
        response = redirect('/')

        # need to validate data
        data_to_validate = {
            "email": req.get('email'),
            "password": req.get('password')
        }

        rules = {"email": "mail",
                 "password": "string|min:5"
                 }

        result, _, errors = validate(req=data_to_validate, rules=rules, return_info=True)
        if not result:
            for key in errors:
                field_name = key
                for k in errors[key]:
                    flash("{0} field {1}".format(field_name, errors[key][k].lower()))

            return redirect('/login')

        try:
            user = loader.load_user_by_email(email=req.get('email'))
            session["username"] = user[0]
        except Exception as e:
            print(e)
            flash("User does not exist.")
            response = redirect('/')

        return response

    @app.route('/logout', methods=['GET'])
    def logout():
        """[summary]

        Returns:
            [type]: [description]
        """
        session["username"] = None

        return redirect('/')

    @app.route('/start-fast', methods=['POST'])
    def start_fast():
        username = auth_check()
        user_loader = UserLoader(get_db_conn())
        fast_loader = FastLoader(get_db_conn(), user_loader)

        saver = FastSaver(get_db_conn(), user_loader, fast_loader)

        try:
            saver.start_fast(email=username)
        except ExceedLimitException:
            flash('This user, {0}, already has an active fast open.'.format(username))
            return redirect('/timer')
        except Exception:
            flash("User does not exist.")
            return redirect('/timer')

        flash("Fast started.")
        return redirect('/timer')

    @app.route('/end-fast', methods=['POST'])
    def end_fast():
        username = auth_check()
        user_loader = UserLoader(get_db_conn())
        fast_loader = FastLoader(get_db_conn(), user_loader)

        saver = FastSaver(get_db_conn(), user_loader, fast_loader)

        try:
            saver.end_fast(email=username)
        except:
            flash("User does not exist.")
            return redirect('/timer')

        flash("Fast Stopped.")
        return redirect('/timer')

    # @app.route('/history/all', methods=['GET'])
    # def history():
    #     loader = FastLoader(get_db_conn())
    #     # pprint(app.jinja_env)
    #     return render_template('index.html', fasts=tuple(loader.load_all()))

    return app
