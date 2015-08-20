#!/usr/bin/env python3

# This is proprietary software.
# Part of cluster monitoring project.
# PEP8 codestyle used, python version 3.

""" Database module. """

import sqlite3
import sqlalchemy as alch

# TODO
class DatabaseManager(object):
    """ Database manager.
        db_manager = DatabaseManager(app)
        conn = db_manager.get_connection()
    """
    def __init__(self, app):
        self.schema_file = open('web_parameters/schema.sql', 'r').read()
        self.conn = None
        # self.engine = alch.create_engine('sqlite:///test_sqlite')

    def close_connect(self):
        """ Close connect. """
        self.conn.commit()
        self.conn.close()

    def drop_table_with_data(self):
        """ Drop table 'entries'. """
        self.conn.execute('drop table if exists users')

# TODO
    def get_connect(self, db_name):
        """ Connect to DATABASE and return it"""
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.conn.cursor().executescript(self.schema_file)
        return self.conn

    def get_all_entries(self, table_name):
        res = self.conn.execute(
            "select * from {}".format(table_name)).fetchall()
        return res

    def insert(self, table_name, data_dict):
        """

        :param table_name:
        :param data_dict:
        :return:
        """
        query = "insert into {} {} values {}"
        column_name = []
        data = []
        for key in data_dict:
            column_name.append(key)
            data.append(data_dict[key])
        query = query.format(table_name, str(tuple(column_name)), str(tuple(data)))
        self.conn.execute(query)