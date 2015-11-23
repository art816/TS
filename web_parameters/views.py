import os
from flask import render_template, request, session, flash, redirect, \
    url_for, abort, g, send_from_directory
from flask import jsonify
from flask import current_app as app
from werkzeug.utils import secure_filename


# TODO сделать разлогинивание при перезапуске сервиса
def show_entries():
    """ Show all entries from database. """
    connect = app.db_manager.get_connect(app.config['DATABASE'])
    cur = connect.execute('select * from users order by id desc')
    entries = cur.fetchall()
    connect.commit()
    connect.close()
    return render_template('show_entries.html',
                           entries=entries)


#TODO make find users in table users
def login():
    """ Login to server. """
    error = None
    if request.method == 'POST':
        #if admin
        if request.form['user_login'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['user_login'] = request.form['user_login']
            session['logged_in'] = True
            session['admin'] = True
            flash('You were logged in')
            return redirect(url_for('start'))
        #if not admin
        if error == 'Invalid username':
            #TODO get logins ones
            users = app.db_manager.get_logins_all_users()
            if request.form['user_login'] not in users:
                error = 'Invalid username'
            elif request.form['password'] != app.db_manager.get_password(
                    request.form['user_login']):
                error = 'Invalid password'
            else:
                session['user_login'] = request.form['user_login']
                session['logged_in'] = True
                session.pop('admin', None)
                flash('You were logged in')
                return redirect(url_for('start'))

    return render_template('login.html', error=error)


def registered_user():
    """
    Registered new users.
    :return:
    """
    if request.method == 'POST':
        user_dict = reformat_request_dict(request.form)
        answer = app.db_manager.register_user(user_dict)
        print('answer=', answer)
        if answer == 'Insert ok':
            flash('You were registered')
            session['user_login'] = request.form['user_login']
            session['logged_in'] = True
            session['admin'] = None
            flash('You were logged in')
            return redirect(url_for('user_data',
                                    user_login=user_dict['user_login']))
        else:
            flash(answer)
            print(answer)
            return render_template('registered.html', user_data=user_dict)
    return render_template('registered.html', user_data=dict())


def reformat_request_dict(request_form):
    data_dict = dict(request_form)
    user_data = dict()
    "Распаковка словаря. По умолчанию значения словаря содержатся в листе"
    for key in data_dict:
        if data_dict[key][0]:
            #экранируем все кавычки
            user_data[key] = data_dict[key][0]
    return user_data


#TODO users must can look your data.
def user_data(user_login):
    """
    Show user data
    user_login
    :return:
    """
    if not session.get('logged_in'):
        abort(401)
    if not session.get('admin'):
        if session.get('user_login') != user_login:
            abort(401)
    print('user_login=', user_login)
    res = app.db_manager.get_entry('users', user_login)
    return render_template('user_data.html', user_data=res[0])


#TODO logout when app is closed.
def logout(*args):
    """ Logout to server. """
    print("logout()")
    session.pop('logged_in', None)
    session.pop('admin', None)
    session.pop('user_login', None)
    # session.pop('user_login', None)
    flash('You were logged out')
    return redirect(url_for('start'))


#old method
def get_num_entries():
    """ Get num entries. """
    connect = app.db_manager.get_connect(app.config['DATABASE'])
    cur = connect.execute('select id from entries order by id desc limit 1')
    id_num = cur.fetchone()['id']
    connect.commit()
    connect.close()
    #import time
    #x = time.time()
    return jsonify({'num_entries': id_num})


#old method
def add_entry():
    """ Add entry. """
    if not session.get('logged_in'):
        abort(401)
    connect = app.db_manager.get_connect(app.config['DATABASE'])
    connect.execute(
        'insert into entries (title, text) values (?, ?)',
        ['{} says'.format(session['user_login']),
         '{}: {}'.format(request.form['title'], request.form['text'])])
    connect.commit()
    connect.close()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


def drop_table(table_name):
    """ Drop table. """
    if not session.get('logged_in'):
        abort(401)
    if not session.get('admin'):
        abort(401)
    app.db_manager.get_connect()
    app.db_manager.drop_table_with_data(table_name)
    flash('Table was dropped')
    return redirect(url_for('start'))


#old method
def show_param(param_name):
    """ """
    #(request.form['param_name'])
    connect = app.db_manager.get_connect(app.config['DATABASE'])
    cur = connect.execute(
        'select * from param where name == "{}" order by id desc'.format(
            param_name))
    param = cur.fetchone()
    print(dir(param))
    #flash(param.name)
    return render_template('show_param.html', param=param)
    #return jsonify({'param': param})


#od method
def update_param():
    """ """
    name = request.form['name']
    with app.db_manager.sessionmaker() as session:
        orm_parameter = session.query(parameter_orm.Parameter).filter_by(
            name=name).one()
        orm_parameter.full_name = request.form['full_name']
        orm_parameter.desc = request.form['desc']
        orm_parameter.identifier = request.form['identifier']
        orm_parameter.units = request.form['units']
        flash('Parameter {} was updated'.format(name))
    return redirect(url_for('show_param', param_name=name))


def start():
    """
    Get start page.
    :return:
    """
    print(request.args)
    return render_template('start.html')


def task(user):
    """
    Get page with task for user=user
    /task/<user>
    :param user:
    :return:
    """
    tasks = []
    users = []

    if not session.get('logged_in'):
        abort(401)
    elif not session.get('admin'):
        if session.get('user_login') != user:
            abort(401)
    else:
        users = app.db_manager.get_logins_all_users()

    #todo make reserved name
    print(app.config["COLOR_SCHEMA"])
    if user == 'admin':
        tasks = app.db_manager.get_all_tasks()
    else:
        tasks = app.db_manager.get_tasks_by_user(user=user)
    return render_template('task.html', tasks=tasks, users=users, color_schema=app.config["COLOR_SCHEMA"])


def add_task():
    """
        Add task for user.
        :return:
    """
    if session.get('admin'):
        if request.method == 'POST':
            user_dict = reformat_request_dict(request.form)
            user_dict['user_value'] = '0'
            answer = app.db_manager.add_task(user_dict)
            print('answer=', answer)
            if answer == 'Insert ok':
                flash(answer)
            else:
                flash(answer)
                print(answer)
            return redirect(url_for('task', user='admin'))
    else:
        abort(401)

def delete_task():
    """
        Add task for user.
        :return:
    """
    if session.get('admin'):
        if request.method == 'POST':
            user_dict = reformat_request_dict(request.form)
            answer = app.db_manager.delete_entry('tasks', user_dict['id'])
            print('answer=', answer)
            if answer == 'Delete ok':
                flash(answer)
            else:
                flash(answer)
                print(answer)
            return redirect(url_for('task', user='admin'))
    else:
        abort(401)

def update_task():
    """
        Add task for user.
        :return:
    """
    if session.get('admin'):
        if request.method == 'POST':
            user_dict = reformat_request_dict(request.form)
            answer = app.db_manager.update_table('tasks',
                                                 user_dict['column_name'],
                                                 user_dict['data'],
                                                 user_dict['id'])
            print('answer=', answer)
            if answer == 'Update ok':
                flash(answer)
            else:
                flash(answer)
                print(answer)
            return redirect(url_for('task', user='admin'))
    else:
        abort(401)



def show_all_users():
    """
        Show data all users.
        :return:
    """
    if not session.get('admin'):
        abort(401)
    res = app.db_manager.get_all_entries('users')
    return render_template('all_user_data.html', user_data=res)

def content():
    """

    :return:
    """
    return render_template("content.html")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def upload_file():

    if request.method == 'POST':
        try:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                user_load_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                                   session.get('user_login'))
                if not os.path.exists(user_load_path):
                    os.mkdir(user_load_path)
                file.save(os.path.join(user_load_path, filename))
                return redirect(url_for('uploaded_file',
                                    name=filename, path='/'+session.get('user_login')))
            else:
                print("ERROR")
        except Exception as e:
            file = request.get_data()
            filename = secure_filename('1111111111111')
            user_load_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                                   session.get('user_login'))

            if not os.path.exists(user_load_path):
                os.mkdir(user_load_path)
            f = open(os.path.join(user_load_path, filename), 'wb')
            f.write(file)
            f.close()
            return redirect(url_for('uploaded_file',
                                    name=filename, path='/'+session.get('user_login')))


    return render_template('upload_file.html')


def uploaded_file_list():
    """

    :return:
    """
    dirs_files = dict()
    for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
        dirs_files[root.replace(app.config['UPLOAD_FOLDER'],'')] = files
    return render_template('uploaded_files.html', dirs_files=dirs_files)


def uploaded_file():
    user_load_path = app.config['UPLOAD_FOLDER'] + request.values['path'].replace('\'','')
    name = request.values['name'].replace('\'','')
    return send_from_directory(user_load_path, name)


def route(configure_app):
    """ Route. """
    configure_app.add_url_rule('/entries', 'show_entries', show_entries)
    configure_app.add_url_rule('/login', 'login',
                               login, methods=['GET', 'POST'])
    configure_app.add_url_rule('/registered_user',
                               'registered_user', registered_user,
                               methods=['GET', 'POST'])
    configure_app.add_url_rule('/user_data/<user_login>', 'user_data',
                               user_data, methods=['GET', 'POST'])
    configure_app.add_url_rule('/logout', 'logout', logout)
    configure_app.add_url_rule('/add', 'add_entry',
                               add_entry, methods=['POST'])
    configure_app.add_url_rule('/drop_table/<table_name>', 'drop_table',
                               drop_table, methods=['GET', 'POST'])
    configure_app.add_url_rule('/show_param/<param_name>', 'show_param',
                               show_param, methods=['GET', 'POST'])
    configure_app.add_url_rule('/update_param', 'update_param',
                               update_param, methods=['GET', 'POST'])
    configure_app.add_url_rule('/start', 'start', start)
    configure_app.add_url_rule('/task/<user>', 'task', task)
    configure_app.add_url_rule('/show_all_users', 'show_all_users',
                               show_all_users)
    configure_app.add_url_rule('/add_task', 'add_task',
                               add_task, methods=['POST'])
    configure_app.add_url_rule('/update_task', 'update_task',
                               update_task, methods=['POST'])
    configure_app.add_url_rule('/delete_task', 'delete_task',
                               delete_task, methods=['POST'])
    configure_app.add_url_rule('/content', 'content',
                               content, methods=['GET'])
    configure_app.add_url_rule('/upload_file', 'upload_file',
                               upload_file, methods=['GET', 'POST'])
    configure_app.add_url_rule('/uploaded_file', 'uploaded_file',
                               uploaded_file, methods=['GET'])
    configure_app.add_url_rule('/uploaded_files', 'uploaded_files',
                               uploaded_file_list, methods=['GET', 'POST'])
    # Json
    configure_app.add_url_rule('/get_num_entries', 'get_num_entries',
                               get_num_entries)


