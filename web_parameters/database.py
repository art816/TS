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
    #TODO
    """
    Сделать коннект к базе данных при старте сервиса.
    Получать имя базы данных в этот же момент.
    """
    def __init__(self, app):
        self.schema_file = open('web_parameters/schema.sql', 'r').read()
        self.conn = None
        self.db_name = app.db_name
        # self.get_connect(app.config['DATABASE'])
        # self.engine = alch.create_engine('sqlite:///test_sqlite')

    def close_connect(self):
        """ Close connect. """
        self.conn.commit()
        self.conn.close()

    def drop_table_with_data(self):
        """ Drop table 'entries'. """
        self.conn.execute('drop table if exists users')
        self.conn.commit()
        print("DROP USERS")

    # TODO
    def get_connect(self):
        """ Connect to DATABASE and return it"""
        self.conn = sqlite3.connect(self.db_name)
        print(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.conn.cursor().executescript(self.schema_file)
        return self.conn

    def get_all_entries(self, table_name):
        res = self.conn.execute(
            "select * from {}".format(table_name)).fetchall()
        self.conn.commit()
        return res

    def get_entry(self, table_name, user_name, user_s_name):

        query = "select * from {} where user_name='{}' and user_s_name='{}'".format(
                table_name, user_name, user_s_name)
        print(query)
        res = self.conn.execute(query).fetchall()
        self.conn.commit()
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
        print(query)
        # self.get_connect()
        try:
            self.conn.execute(query)
            self.conn.commit()
        except sqlite3.IntegrityError:
            return "You try insert not unique user"

    def register_user(self, data_dict):
        """

        :param data_dict:
        :return:
        """
        "Распаковка словаря. По умолчанию значения словаря содержатся в листе"
        for key in data_dict:
            data_dict[key] = data_dict[key][0]
        return self.insert('users', data_dict)
