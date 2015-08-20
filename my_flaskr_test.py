# Testing mini project show_device_from_NMS

import unittest
from flask import Flask, g
import sqlite3

from web_parameters import database
from web_parameters import show_device_from_NMS
from web_parameters import parameter_orm


class FlaskrTestCase(unittest.TestCase):
    """ Test flaskr. """
    def setUp(self):
        app = show_device_from_NMS.configure_app()
        self.db_name = app.config['DATABASE']
        app.config['TESTING'] = True
        self.app_test_client = app.test_client()
        self.app_test_client.db_manager = app.db_manager
        # context_creator = ContextCreator('buer')
        # self.context = context_creator.from_file()

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
        self.login('user', '111111')
        string_with_data = self.get_data_from_page('/start')
        self.assertTrue('Task' in string_with_data)

    def test_login(self):
        """ """
        rv = self.login('user', '111111')
        self.assertTrue('You were logged in' in str(rv.data))
        rv = self.logout()
        self.assertTrue('You were logged out' in str(rv.data))
        rv = self.login('adminx', 'default')
        self.assertTrue('Invalid username' in str(rv.data))
        rv = self.login('user', 'defaultx')
        self.assertTrue('Invalid password' in str(rv.data))

    def login(self, username, password):
        return self.app_test_client.post('/login', data=dict(
                    username=username,
                    password=password
                    ), follow_redirects=True)
    
    def logout(self):
        return self.app_test_client.get('/logout', follow_redirects=True)

    def registered(self, user_dict):
        return self.app_test_client.post('/registered_user', user_dict,
            follow_redirects=True)

    def test_registered(self):
        """
        """
        user_dict = dict(user_name='art212321',
                          user_s_name='123',
                          user_password='art',
                          user_class=12,
                          user_mail='1233@ase')
        rv = self.registered(user_dict)
        self.assertTrue('You were registered' in str(rv.data))


    def test_messages(self):
        self.app_test_client.db_manager.get_connect(self.db_name)
        self.app_test_client.db_manager.drop_table_with_data()
        
        self.login('user','111111')
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
        self.db_name = self.app.config['DATABASE']
        self.db_manager = database.DatabaseManager(self.app)

    def tearDown(self):
        """ """
        self.db_manager.close_connect()

    def test_init_db(self):
        """ Get db. """
        self.assertTrue(self.db_manager.get_connect(self.db_name))

    def test_insert(self):
        """

        :return:
        """
        connect = self.db_manager.get_connect(self.db_name)
        connect.execute("insert into users (user_name, user_s_name, user_password) values (?, ?, ?)",
                        ['art', 'art', 'art'])
        entries = self.db_manager.get_all_entries('users')
        self.assertEqual((entries[-1]['user_name'], entries[-1]['user_password']),
                         ('art', 'art'))

    def test_double_insert(self):
        """
        Try insert two entries with idential user_name
        :return:
        """
        connect = self.db_manager.get_connect(self.db_name)
        connect.execute(("insert into users (user_name, user_s_name, user_password)"
                         "values (?, ?, ?)"),
                        ['art5', 'art', 'art'])
        try:
            connect.execute(("insert into users (user_name, user_s_name, user_password)"
                             " values (?, ?, ?)"),
                            ['art5', 'art', 'art'])
        except sqlite3.IntegrityError:
            print("You try insert not unique user")
        else:
            self.assertTrue(False, "insert not unique user")


    #TODO nothing assert
    def test_drop_table(self):
        """ Drop table. """
        self.db_manager.get_connect(self.db_name)
        self.assertTrue(hasattr(self.db_manager, 'conn'))
        self.db_manager.drop_table_with_data()

    def test_get_all_data(self):
        """
        :return:
        """
        table_name = 'users'
        first_data = dict(id=1,
                          user_name='art2',
                          user_s_name='123',
                          user_password='art',
                          user_class=12,
                          user_mail='1233@ase')
        second_data = dict(id=2,
                           user_name='art3',
                           user_s_name='123',
                           user_password='art',
                           user_class=12,
                           user_mail='1233@ase')
        self.db_manager.get_connect(self.db_name)
        self.db_manager.drop_table_with_data()
        self.db_manager.get_connect(self.db_name)
        self.db_manager.insert(table_name, first_data)
        self.db_manager.insert(table_name, second_data)
        res = self.db_manager.get_all_entries('users')
        list_res = list(res)
        self.assertEqual(dict(list_res[0]), first_data)
        self.assertEqual(dict(list_res[1]), second_data)
        self.assertEqual(len(list_res), 2)


        
if __name__ == '__main__':
    unittest.main()

