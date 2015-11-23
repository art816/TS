""" Config for app. """
import os

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
USERNAME = 'admin'
PASSWORD = '111111'
TEST_DATABASE = 'test_sqlite'
DATABASE = 'curent_database'
COLOR_SCHEMA = {0:'white',
                1:'red',
                2:'orange',
                3:'yellow',
                4:'blue',
                5:'green'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'load_files')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
