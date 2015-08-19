#rom app import app
from flask import render_template, request, session, flash, redirect, url_for, abort, g

import sys
sys.path.append('../NMS')
#sys.path.append('app/templates')

from nms.core.context import ContextCreator


def route(db_manager):
    """ Route. """
    @db_manager.app.route('/')
    @db_manager.app.route('/index')
    def index():
        """ Show all device and parameters from buer_context"""
        context_creator = ContextCreator('buer')
        context = context_creator.from_file()
        db = db_manager.get_db()
        for device in context.devices:
            for param in context.devices[device].params_dict.values():
                db.execute(
                    'insert into entries (title, text) values (?, ?)',
                    [param.name, param.value])
        db.commit()
        db.close()
        return render_template('index.html',
                               title='Home',
                               devices=context.devices)

    @db_manager.app.route('/entries')
    def show_entries():
        """ Show all entries from database. """
        db = db_manager.get_db()
        cur = db.execute('select id, title, text from entries order by id desc')
        entries = cur.fetchall()
        db.commit()
        db.close()
        return render_template('show_entries.html', entries=entries)

    @db_manager.app.route('/login', methods=['GET', 'POST'])
    def login():
        """ Login to server. """
        error = None
        if request.method == 'POST':
            if request.form['username'] != db_manager.app.config['USERNAME']:
                error = 'Invalid username'
            elif request.form['password'] != db_manager.app.config['PASSWORD']:
                error = 'Invalid password'
            else:
                session['user_name'] = request.form['username']
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('show_entries'))
        return render_template('login.html', error=error)

    @db_manager.app.route('/logout')
    def logout():
        """ Logout to server. """
        session.pop('logged_in', None)
        flash('You were logged out')
        return redirect(url_for('show_entries'))


    @db_manager.app.route('/add', methods=['POST'])
    def add_entry():
        """ Add entry. """
        if not session.get('logged_in'):
            abort(401)
        db = db_manager.get_db()
        db.execute(
            'insert into entries (title, text) values (?, ?)',
            ['{} says'.format(session['user_name']), 
             '{}: {}'.format(request.form['title'], request.form['text'])])
        db.commit()
        db.close()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))

    @db_manager.app.route('/drop', methods=['POST'])
    def drop_entry():
        """ Drop entries. """
        if not session.get('logged_in'):
            abort(401)
        db_manager.get_db()
        db_manager.drop_db()
        flash('Table was dropped') 
        return redirect(url_for('show_entries'))

