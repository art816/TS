# Testing mini project show_device_from_NMS

import unittest
from flask import Flask, g
import sys
sys.path.append('../NMS')

from nms.core.context import ContextCreator
from web_parameters import database
from web_parameters import show_device_from_NMS
from nms.core.parameters import configure_parameters
from web_parameters import parameter_orm


class FlaskrTestCase(unittest.TestCase):
    """ Test flaskr. """
    def setUp(self):
        app = show_device_from_NMS.configure_app()
        self.db_name = app.config['DATABASE']
        app.config['TESTING'] = True
        self.app_test_client = app.test_client()
        self.app_test_client.db_manager = app.db_manager
        context_creator = ContextCreator('buer')
        self.context = context_creator.from_file()

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
        for url in ['/entries']:
            return_data = self.app_test_client.get(url)
            string_with_data = str(return_data.data)
            for device in self.context.devices:
                for param in self.context.devices[device].params_dict:
                    self.assertTrue(param in string_with_data)
    
    def test_login(self):
        """ """
        rv = self.login('user', '111111')
        self.assertTrue( 'You were logged in' in str(rv.data))
        rv = self.logout()
        self.assertTrue( 'You were logged out' in str(rv.data))
        rv = self.login('adminx', 'default')
        self.assertTrue( 'Invalid username' in str(rv.data))
        rv = self.login('user', 'defaultx')
        self.assertTrue( 'Invalid password' in str(rv.data))

    def login(self, username, password):
        return self.app_test_client.post('/login', data=dict(
                    username=username,
                    password=password
                    ), follow_redirects=True)
    
    def logout(self):
        return self.app_test_client.get('/logout', follow_redirects=True)

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
        context_creator = ContextCreator('buer')
        self.context = context_creator.from_file()
        self.db_manager = database.DatabaseManager(self.app)

    def tearDown(self):
        """ """
        self.db_manager.close_connect()

    def test_init_db(self):
        """ Get db. """
        self.assertTrue(self.db_manager.get_connect(self.db_name))

    def test_drop_table(self):
        """ Drop table. """
        self.db_manager.get_connect(self.db_name)
        self.assertTrue(hasattr(self.db_manager, 'conn'))
        self.db_manager.drop_table_with_data()
        
if __name__ == '__main__':
    unittest.main()

