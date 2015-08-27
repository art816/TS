# Testing mini project show_device_from_NMS

import unittest
from flask import Flask, g
import sqlite3

from web_parameters import database
from web_parameters import show_device_from_NMS
from web_parameters import parameter_orm


class FlaskrTestCase(unittest.TestCase):
    """ Test flaskr. """

    @classmethod
    def setUpClass(cls):
        app = show_device_from_NMS.configure_app(db_name='TEST_DATABASE')
        # self.app.db_name = app.config['TEST_DATABASE']
        app.config['TESTING'] = True
        cls.app_test_client = app.test_client()
        cls.app_test_client.db_manager = app.db_manager
        cls.app_test_client.db_manager.get_connect()
        # context_creator = ContextCreator('buer')
        # self.context = context_creator.from_file()

    @classmethod
    def tearDownClass(cls):
        """ """
        cls.app_test_client.db_manager.drop_table_with_data('users')
        cls.app_test_client.db_manager.close_connect()


    def test_empty_list_of_devices(self):
        """ Get davice name. """
        for url in ['/', '/index']:
            return_data = self.app_test_client.get(url)
            string_with_data = str(return_data.data)
            for device in configure_parameters():
                self.assertTrue(device in string_with_data)

    def test_entries(self):
        """ Get all data from /entries.
            Assert add new entries. """
        string_with_data = self.get_data_from_page('/entries')
        for device in self.context.devices:
            for param in self.context.devices[device].params_dict:
                self.assertTrue(param in string_with_data)

    def get_data_from_page(self, url):
        """
        Return str with data from page(url)
        """
        return_data = self.app_test_client.get(url)
        return str(return_data.data)

    def test_visible_parameter(self):
        self.logout()
        string_with_data = self.get_data_from_page('/start')
        self.assertFalse('Task' in string_with_data)
        self.login('admin', '111111')
        string_with_data = self.get_data_from_page('/start')
        self.assertTrue('Task' in string_with_data)

    def test_login(self):
        """ """
        rv = self.login('admin', '111111')
        self.assertTrue('You were logged in' in str(rv.data))
        self.assertTrue('Admin=admin' in str(rv.data))
        rv = self.logout()
        self.assertTrue('You were logged out' in str(rv.data))
        rv = self.login('adminx', 'default')
        self.assertTrue('Invalid username' in str(rv.data))
        rv = self.login('admin', 'defaultx')
        self.assertTrue('Invalid password' in str(rv.data))
        user_dict = dict(
            user_login='2123',
            user_name='art212321',
            user_s_name='123123',
            user_password='art',
            user_class=12,
            user_mail='1233@ase')
        rv = self.registered(user_dict)
        self.assertTrue('You were registered' in str(rv.data))
        rv = self.login('2123', 'art')
        self.assertTrue('You were logged in' in str(rv.data))



    def login(self, username, password):
        return self.app_test_client.post('/login',
            data=dict(
                user_login=username,
                password=password
            ), follow_redirects=True)

    def logout(self):
        return self.app_test_client.get('/logout', follow_redirects=True)

    def registered(self, user_dict):
        return self.app_test_client.post('/registered_user', data=user_dict,
            follow_redirects=True)

    def test_registered(self):
        """
        """
        user_dict = dict(
            user_login='2123',
            user_name='art212321',
            user_s_name='123123',
            user_password='art',
            user_class=12,
            user_mail='1233@ase')
        rv = self.registered(user_dict)
        self.assertTrue('You were registered' in str(rv.data))
        for val in user_dict.values():
            self.assertTrue(str(val) in str(rv.data))
        #test add user in user_list


    def test_messages(self):
        # self.app_test_client.db_manager.get_connect()
        # self.app_test_client.db_manager.drop_table_with_data()
        
        self.login('admin','111111')
        rv = self.app_test_client.post('/add', data=dict(
                    title='<Hello>',
                    text='<strong>HTML</strong> allowed here'
                    ), follow_redirects=True)
        self.assertTrue( 'No entries here so far' not in str(rv.data))
        self.assertTrue( '&lt;Hello&gt;' in str(rv.data))
        self.assertTrue('strong&gt;HTML&lt;/strong&gt; allowed here' in str(rv.data))

    def test_show_parameter(self):
        """ """
        rv = self.app_test_client.get('/show_param/memOccPercent')
        self.assertTrue('200' in str(rv))

    def test_update_parameter(self):
        """ """

    def test_show_user_data(self):
        """ """
        rv = self.app_test_client.get('/show_all_users')
        self.assertTrue('200' in str(rv))
        


class TestORM(unittest.TestCase):
    """ Test ORM. """
    def setUp(self):
        """ """ 
        self.parameter_dict = configure_parameters()

    def test_create_object_parameter(self):
        param = parameter_orm.Parameter('1','1','1','1','1', '1')
        self.assertTrue('identifier' in dir(param))
        self.assertTrue(param.identifier == '1')

    def test_create_orm_parameters_dict(self):
        """ """
        orm_parameters = parameter_orm.create_orm_parameters_dict(self.parameter_dict)
        self.assertEqual(sorted(list(self.parameter_dict.keys())), 
                         sorted(list(orm_parameters)))

    def test_create_orm_parameter(self):
        """ """
        name_list = list(self.parameter_dict.keys())
        param = parameter_orm.create_orm_parameter(self.parameter_dict[name_list[1]])
        self.assertEqual(type(param), parameter_orm.Parameter)
        self.assertEqual(param.name, self.parameter_dict[name_list[1]].name)

    @unittest.skip('asdfasf')
    def test_add_orm_parameter_in_db(self):
        """ """
        app = show_device_from_NMS.configure_app()
        orm_parameters = parameter_orm.create_orm_parameters_dict(self.parameter_dict)
        with app.db_manager.sessionmaker() as session:
            for orm_param in orm_parameters.values():
                session.add(orm_param)
        app.orm_parameters = orm_parameters


class DBTest(unittest.TestCase):
    """ Test database. """
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object('web_parameters.config')
        self.app.db_name = self.app.config['TEST_DATABASE']
        self.app.db_manager = database.DatabaseManager(self.app)

    def tearDown(self):
        """ """
        self.app.db_manager.close_connect()

    def test_init_db(self):
        """ Get db. """
        self.assertTrue(self.app.db_manager.get_connect())

    def test_insert(self):
        """

        :return:
        """
        self.app.db_manager.drop_table_with_data('users')
        user_dict = dict(
            user_login='art',
            user_name='art',
            user_s_name='art',
            user_password='art',
            user_class=12,
            user_mail='1233@ase')
        self.app.db_manager.insert('users', user_dict)
        entries = self.app.db_manager.get_all_entries('users')
        self.assertEqual((entries[-1]['user_name'], entries[-1]['user_password']),
                         ('art', 'art'))

    def test_get_entry(self):
        """
        :return:
        """
        user_dict = dict(
            user_login='art',
            user_name='art',
            user_s_name='art',
            user_password='art',
            user_class=12,
            user_mail='1233@ase')
        self.app.db_manager.insert('users', user_dict)
        entries = self.app.db_manager.get_entry('users', 'art')
        self.assertEqual((entries[0]['user_name'], entries[0]['user_password']),
                         ('art', 'art'))
        self.assertEqual(len(entries), 1)

    def test_double_insert(self):
        """
        Try insert two entries with idential user_name
        :return:
        """
        user_dict = dict(
            user_login='123213',
            user_name='art5',
            user_s_name='123',
            user_password='art',
            user_class=12,
            user_mail='1233@ase')
        self.app.db_manager.insert('users', user_dict)
        self.assertEqual(self.app.db_manager.insert('users', user_dict),
                         "You try insert not unique user",
                         "insert not unique user")


    #TODO nothing assert
    def test_drop_table(self):
        """ Drop table. """
        self.assertTrue(hasattr(self.app.db_manager, 'conn'))
        self.app.db_manager.drop_table_with_data('users')

    def test_get_all_data(self):
        """
        :return:
        """
        table_name = 'users'
        first_data = dict(
            id=1,
            user_login='2',
            user_name='art2',
            user_s_name='123',
            user_password='art',
            user_class=12,
            user_mail='1233@ase')
        second_data = dict(
            id=2,
            user_login='3',
            user_name='art3',
            user_s_name='123',
            user_password='art',
            user_class=12,
            user_mail='1233@ase')
        self.app.db_manager.drop_table_with_data('users')
        self.app.db_manager.insert(table_name, first_data)
        self.app.db_manager.insert(table_name, second_data)
        res = self.app.db_manager.get_all_entries('users')
        list_res = list(res)
        self.assertEqual(dict(list_res[1]), first_data)
        self.assertEqual(dict(list_res[0]), second_data)
        self.assertEqual(len(list_res), 2)

    def test_get_logins(self):
        """
        :return:
        """
        table_name = 'users'
        first_data = dict(
            id=1,
            user_login='21214',
            user_name='art2',
            user_s_name='123',
            user_password='art',
            user_class=12,
            user_mail='1233@ase')
        second_data = dict(
            id=2,
            user_login='3',
            user_name='art3',
            user_s_name='123',
            user_password='art',
            user_class=12,
            user_mail='1233@ase')
        self.app.db_manager.drop_table_with_data('users')
        self.app.db_manager.insert(table_name, first_data)
        self.app.db_manager.insert(table_name, second_data)
        res = self.app.db_manager.get_logins_all_users()
        self.assertTrue(first_data['user_login'] in res, res)
        self.assertTrue(second_data['user_login'] in res, res)
        self.assertEqual(len(res), 2)

    def test_get_password(self):
        """
        :return:
        """
        table_name = 'users'
        user_data = dict(
            id=1,
            user_login='21214',
            user_name='art2',
            user_s_name='123',
            user_password='art',
            user_class=12,
            user_mail='1233@ase')
        self.app.db_manager.drop_table_with_data('users')
        self.app.db_manager.insert(table_name, user_data)
        res = self.app.db_manager.get_password(user_data['user_login'])
        self.assertTrue(user_data['user_password'] in res, res)

    def test_get_all_tasks(self):
        """

        :return:
        """
        self.app.db_manager.drop_table_with_data('tasks')
        data_dict = {'user_login': '1341341234', 'user_task': 'qwefqwefqwef'}
        self.assertEqual(self.app.db_manager.add_task(data_dict), 'Insert ok')
        res = self.app.db_manager.get_all_tasks()
        self.assertTrue(len(res) == 1, len(res))
        self.assertTrue(res[0]['user_login'] == '1341341234')

    def test_update_table(self):
        """

        :return:
        """
        self.app.db_manager.drop_table_with_data('tasks')
        data_dict = {'user_login': '1341341234', 'user_task': 'qwefqwefqwef'}
        self.assertEqual(self.app.db_manager.add_task(data_dict), 'Insert ok')
        res = self.app.db_manager.get_all_tasks()
        self.assertTrue(res[0]['user_login'] == '1341341234')
        self.assertTrue(len(res) == 1, len(res))
        self.assertEqual(self.app.db_manager.update_table('tasks', 'user_login', 'qwe', 1), 'Update ok')
        res = self.app.db_manager.get_all_tasks()
        self.assertTrue(res[0]['user_login'] == 'qwe')
        self.assertTrue(len(res) == 1, len(res))


    def test_delete_entry(self):
        """

        :return:
        """
        self.app.db_manager.drop_table_with_data('tasks')
        data_dict = {'user_login': '1341341234', 'user_task': 'qwefqwefqwef'}
        self.assertEqual(self.app.db_manager.add_task(data_dict), 'Insert ok')
        res = self.app.db_manager.get_all_tasks()
        self.assertTrue(res[0]['user_login'] == '1341341234')
        self.assertTrue(len(res) == 1, len(res))
        self.assertEqual(self.app.db_manager.delete_entry('tasks', 1), 'Delete ok')
        res = self.app.db_manager.get_all_tasks()
        self.assertTrue(len(res) == 0, len(res))






if __name__ == '__main__':
    unittest.main()

