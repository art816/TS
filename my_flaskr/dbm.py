import sqlite3
from flask import g

class DBM(object):

    def __init__(self, app):
        """ """
        self.app = app
        self.schema_file = open('my_flaskr/schema.sql', 'r').read()

    def close_db(self):
        """ """
        self.conn.commit
        self.conn.close
    
    def drop_db(self):
        """ """
        self.conn.execute('drop table if exists entries')
        self.close_db()

    def get_db(self):
        """Соединяет с указанной базой данных."""
        self.conn = sqlite3.connect(self.app.config['DATABASE'])
        self.conn.row_factory = sqlite3.Row
        self.conn.cursor().executescript(self.schema_file)
        return self.conn



