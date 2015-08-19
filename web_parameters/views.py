#rom app import app
from flask import render_template, request, session, flash, redirect, url_for, abort, g
from flask import jsonify

import sys
sys.path.append('../NMS')
#sys.path.append('app/templates')

from nms.core.context import ContextCreator
from flask import current_app as app
from web_parameters import parameter_orm
from nms.core.parameters import configure_parameters

#@app.route('/')
#@app.route('/inodex')
def index():
    """ Show all device and parameters from buer_context"""
    table_param_dict = dict()
    with app.db_manager.sessionmaker() as session:
        session.expire_on_commit = False
        for orm_param in session.query(parameter_orm.Parameter).all():
            table_param_dict[orm_param.name] = orm_param
        if not table_param_dict:
            table_param_dict = parameter_orm.create_orm_parameters_dict(configure_parameters())
            for orm_param in table_param_dict.values():
                session.add(orm_param)
        param_name_list = [param_name.upper()[:3] for param_name in table_param_dict]
        param_name_list = sorted(list(set(param_name_list)))
    return render_template('index.html',
                           title='Home',
                           parameters=table_param_dict,
                           param_list=param_name_list)

#@app.route('/entries')
def show_entries():
    """ Show all entries from database. """
    connect= app.db_manager.get_connect(app.config['DATABASE'])
    cur = connect.execute('select id, title, text from entries order by id desc')
    entries = cur.fetchall()
    connect.commit()
    connect.close()
    return render_template('show_entries.html',
                           entries=entries)
     #                      num_entries=num_entries)

#@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login to server. """
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['user_name'] = request.form['username']
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

#@app.route('/logout')
def logout():
    """ Logout to server. """
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

#@app.route('/get_num_entries')
def get_num_entries():
    """ Get num entries. """
    connect= app.db_manager.get_connect(app.config['DATABASE'])
    cur = connect.execute('select id from entries order by id desc limit 1')
    id_num = cur.fetchone()['id']
    connect.commit()
    connect.close()
    #import time
    #x = time.time()
    return jsonify({'num_entries': id_num})


#@app.route('/add', methods=['POST'])
def add_entry():
    """ Add entry. """
    if not session.get('logged_in'):
        abort(401)
    connect = app.db_manager.get_connect(app.config['DATABASE'])
    connect.execute(
        'insert into entries (title, text) values (?, ?)',
        ['{} says'.format(session['user_name']), 
         '{}: {}'.format(request.form['title'], request.form['text'])])
    connect.commit()
    connect.close()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

#@app.route('/drop', methods=['POST'])
def drop_entry():
    """ Drop entries. """
    if not session.get('logged_in'):
        abort(401)
    app.db_manager.get_connect(app.config['DATABASE'])
    app.db_manager.drop_table_with_data()
    flash('Table was dropped') 
    return redirect(url_for('show_entries'))

def show_param(param_name):
    """ """
    #(request.form['param_name'])
    connect = app.db_manager.get_connect(app.config['DATABASE'])
    cur = connect.execute('select * from param where name == "{}" order by id desc'.format(param_name))
    param = cur.fetchone()
    print(dir(param))
    #flash(param.name)
    return render_template('show_param.html', param=param)
    #return jsonify({'param': param})

def update_param():
    """ """
    name = request.form['name']
    with app.db_manager.sessionmaker() as session:
        orm_parameter = session.query(parameter_orm.Parameter).filter_by(name=name).one()
        orm_parameter.full_name = request.form['full_name']
        orm_parameter.desc = request.form['desc']
        orm_parameter.identifier = request.form['identifier']
        orm_parameter.units = request.form['units']
        flash('Parameter {} was updated'.format(name))
    return redirect(url_for('show_param', param_name=name))

#def update_param():
 #   (request.form['param_name'])


def route(app):
    """ Route. """
    app.add_url_rule('/', 'main', index)
    app.add_url_rule('/index', 'main', index)
    app.add_url_rule('/entries', 'show_entries', show_entries)
    app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/add', 'add_entry', add_entry, methods=['POST'])
    app.add_url_rule('/drop', 'drop_entry', drop_entry, methods=['POST'])
    app.add_url_rule('/show_param/<param_name>', 'show_param', show_param, methods=['GET', 'POST'])
    app.add_url_rule('/update_param', 'update_param', update_param, methods=['GET', 'POST'])

    # Json
    app.add_url_rule('/get_num_entries', 'get_num_entries', get_num_entries)


