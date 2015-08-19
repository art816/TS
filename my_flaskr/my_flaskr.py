#!/usr/bin/env python3
import sqlite3
from flask import Flask, g
from my_flaskr import views
from my_flaskr import dbm

app = Flask(__name__)
app.config.from_object('my_flaskr.config')


db_manager = dbm.DBM(app)
views.route(db_manager)   
