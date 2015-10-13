#!/usr/bin/env python3

from flask import Flask, g
from web_parameters import views
from web_parameters import database
import os
#from web_parameters import parameter_orm
#from nms.core.parameters import configure_parameters


def configure_app(db_name=None):
    app = Flask(__name__)
    app.config.from_object('web_parameters.config')
    if db_name == 'TEST_DATABASE':
        app.db_name = app.config['TEST_DATABASE']
    elif db_name:
        app.db_name = db_name
    else:
        app.db_name = app.config['DATABASE']
    app.db_manager = database.DatabaseManager(app)
    # app.secret_key = os.urandom(32)
    print('secret_key=', app.secret_key)
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        app.db_manager.close_connect()

    views.route(app)
    return app


def run_server():
    print("rrrrrrrrrrrrrruuuuuuuunnnnnnnnn")
    app = configure_app()
    # app.do_teardown_appcontext = views.logout
    app.run(debug=True, )


def main():
    run_server()


