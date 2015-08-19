#!/usr/bin/env python3
import sqlite3
from flask import Flask, g
from web_parameters import views
#from web_parameters import database
#from web_parameters import parameter_orm
#from nms.core.parameters import configure_parameters


def configure_app():
    app = Flask(__name__)
    app.config.from_object('web_parameters.config')
    #app.db_manager = database.DatabaseManager(app)
    views.route(app)   
    return app


def run_server():
    app = configure_app()
    app.run(debug=True)


def main():
    run_server()


