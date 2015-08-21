#!/usr/bin/env python3
import sqlite3
from flask import Flask, g
from web_parameters import views
from web_parameters import database
#from web_parameters import parameter_orm
#from nms.core.parameters import configure_parameters


def configure_app(db_name = None):
    app = Flask(__name__)
    app.config.from_object('web_parameters.config')
    if db_name == 'TEST_DATABASE':
        app.db_name = app.config['TEST_DATABASE']
    elif db_name:
        app.db_name = db_name
    else:
        app.db_name = app.config['DATABASE']
    app.db_manager = database.DatabaseManager(app)
    views.route(app)   
    return app


def run_server():
    app = configure_app()
    app.db_manager.get_connect()
    app.run(debug=True, )


def main():
    run_server()


