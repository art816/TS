#!/usr/bin/env python3

# This is proprietary software.
# Part of cluster monitoring project.
# PEP8 codestyle used, python version 3.

""" Database module. """

import sqlite3
import time
# import sqlalchemy as alch


# TODO
class DatabaseManager(object):
    """ Database manager.
        db_manager = DatabaseManager(app)
        conn = db_manager.get_connection()
    """
    # TODO
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

    def close_connect(self, *args):
        """ Close connect. """
        print("close")
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def drop_table_with_data(self, table_name):
        """ Drop table 'entries'. """
        self.get_connect()
        query = "drop table if exists '{}'".format(
            table_name.replace('\'', '').replace('\"', ''))
        self.conn.execute(query)
        self.close_connect()
        print("DROP USERS")

    # TODO
    def get_connect(self):
        """ Connect to DATABASE and return it"""
        print(sqlite3.__doc__)
        self.conn = sqlite3.connect(self.db_name)
        print(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.conn.cursor().executescript(self.schema_file)
        print("try get connect")
        return self.conn

    def get_all_entries(self, table_name):
        self.get_connect()
        res = self.conn.execute(
            "select * from '{}' order by id desc".format(
                table_name.replace('\'', '').replace('\"', ''))).fetchall()
        self.close_connect()
        return res

    def get_entry(self, table_name, user_login):
        self.get_connect()
        query = "select * from '{}' where user_login='{}' order by id desc".format(
            table_name.replace('\'', '').replace('\"', ''),
            user_login.replace('\'', '').replace('\"', ''))
        print(query)
        res = self.conn.execute(query).fetchall()
        self.close_connect()
        return res

    def get_logins_all_users(self):
        self.get_connect()
        query = "select user_login from users"
        res = self.conn.execute(query).fetchall()
        self.close_connect()
        return [entry['user_login'] for entry in res]

    def get_password(self, user_login):
        self.get_connect()
        query = "select user_password from users where user_login='{}'".format(
            user_login.replace('\'', '').replace('\"', ''))
        res = self.conn.execute(query).fetchall()
        self.close_connect()
        assert (len(res) == 1)
        return res[0]['user_password']

    def insert(self, table_name, data_dict):
        """

        :param table_name:
        :param data_dict:
        :return:
        """
        query = "insert into '{}' {} values {}"
        column_name = []
        data = []
        for key in data_dict:
            column_name.append(str(key).replace('\'', '').replace('\"', ''))
            data.append(str(data_dict[key]).replace('\'', '').replace('\"', ''))
        query = query.format(
            table_name,
            str(tuple(column_name)),
            str(tuple(data)))
        #('qewe',) -> ('qewe')
        query = query.replace(',)', ')')
        print(query)
        # self.get_connect()
        try:
            self.get_connect()
            self.conn.execute(query)
            self.close_connect()
        except sqlite3.IntegrityError as answer:
            for res in answer.args:
                print(res)
                if 'UNIQUE constraint failed' in res:
                    ind = res[::-1].find('.')
                    #TODO make for double unique
                    return "You try insert not unique user: {}".format(
                        res[len(res)-ind:])
                if 'NOT NULL constraint failed' in res:
                    ind = res.find('.')
                    return 'NOT NULL constraint failed: {}'.format(
                        res[ind+1:])
        else:
            return 'Insert ok'

    def register_user(self, data_dict):
        """
        :param data_dict:
        :return:
        """
        return self.insert('users', data_dict)

    def add_task(self,  data_dict):
        """
        :param data_dict:
        :return:
        """
        data_dict['time'] = time.ctime(time.time())
        return self.insert('tasks', data_dict)

    def get_all_tasks(self):
        """
        :return: List of sql_dictionary
        """
        res = self.get_all_entries('tasks')
        return res

    def get_tasks_by_user(self, user):
        """
        :return: List of sql_dictionary
        """
        res = self.get_entry('tasks', user)
        return res


    #TODO test
    def update_table(self, table_name, column_name, data, id):
        """

        :param table:
        :param column:
        :param data:
        :return:
        """
        query = "update '{}' set '{}'='{}' where id='{}'"
        # for key in data_dict:
        #     column_name.append(str(key).replace('\'', '').replace('\"', ''))
        #     data.append(str(data_dict[key]).replace('\'', '').replace('\"', ''))

        query = query.format(
            table_name,
            column_name,
            data,
            id)

        try:
            self.get_connect()
            self.conn.execute(query)
            self.close_connect()
        except sqlite3.IntegrityError as answer:
            pass
        else:
            return 'Update ok'

    #TODO test
    def delete_entry(self, table_name, id):
        """

        :param table:
        :param column:
        :param data:
        :return:
        """
        query = "delete from '{}' where id='{}'"
        query = query.format(table_name, id)
        try:
            self.get_connect()
            self.conn.execute(query)
            self.close_connect()
        except sqlite3.IntegrityError as answer:
            pass
        else:
            return 'Delete ok'

    def parser_args(self):
        pass