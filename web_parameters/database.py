#!/usr/bin/env python3

# This is proprietary software.
# Part of cluster monitoring project.
# PEP8 codestyle used, python version 3.

""" Database module. """

import sqlite3

from nms.core.database import SafeSession
from web_parameters.parameter_orm import BASE
import sqlalchemy as alch
from sqlalchemy.orm.session import Session

# TODO
class DatabaseManager(object):
    """ Database manager.
        db_manager = DatabaseManager(app)
        conn = db_manager.get_connection()
    """
    def __init__(self, app):
        self.schema_file = open('web_parameters/schema.sql', 'r').read()
        self.conn = None
        self.engine = alch.create_engine('sqlite:///test_sqlite')
        BASE.metadata.create_all(bind=self.engine)
        session_factory = alch.orm.sessionmaker(bind=self.engine,
                                       class_=SafeSession)
        # Thread safe session maker
        self.sessionmaker = alch.orm.scoped_session(session_factory)

    def close_connect(self):
        """ Close connect. """
        self.conn.commit()
        self.conn.close()

    def drop_table_with_data(self):
        """ Drop table 'entries'. """
        self.conn.execute('drop table if exists entries')

# TODO
    def get_connect(self, db_name):
        """ Connect to DATABASE and return it"""
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.conn.cursor().executescript(self.schema_file)
        return self.conn

