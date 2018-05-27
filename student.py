# -*- coding: utf-8 -*-
# @Time    : 2018/5/18 16:49
# @Author  : Zhang
# @FileName: student.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
import pymysql
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
import numpy as np

DEBUG = True
db = pymysql.connect(
    host='localhost',
    user='root',
    passwd='0304',
    db='student',
    charset='utf8'
)
g = db.cursor()

'''配置数据库'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'admin'
app.config['DEBUG'] = 'True'


def check_db(query, args=(), one=False):
    cur = g
    g.execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


# 首页
@app.route('/')
def index():
    return render_template('main.html')


def manager_judge():
    if not session['user_id']:
        error = 'Invalid manager, please login'
        return render_template('error.html', error=error)


# 登录页面
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_system'))
    return render_template('login.html', error=error)


@app.route('/system')
def show_system():
    # manager_judge()
    if not session.get('logged_in'):
        error = 'You have to log in'
    else:
        cur = g
        g.execute('select id, name, gender, phone, birthdate, address from student order by id desc')
        all_data = [dict(id=row[0], name=row[1], gender=row[2], phone=row[3], birthdate=row[4], address=row[5]) for row in cur.fetchall()]
        return render_template('admin_control.html', all_data=all_data)
    return render_template('error.html', error=error)


@app.route('/add')
def add_data():
    return render_template('admin_add.html')


@app.route('/delete')
def delete_data():
    return render_template('admin_delete.html')


@app.route('/search')
def search_data():
    return render_template('admin_search.html')


@app.route('/result')
def show_search():
    return render_template('show_search.html')


@app.route('/data/add', methods=['POST'])
def data_add():
    # if not session.get('logged_in'):
    #     abort(401)
        if request.method == 'POST':
            if not request.form['id']:
                error = 'You have to input the student id'
            elif not request.form['name']:
                error = 'You have to input the student name'
            elif not request.form['gender']:
                error = 'You have to input the student gender'
            elif not request.form['birthdate']:
                error = 'You have to input the student birthdate'
            elif not request.form['phone']:
                error = 'You have to input the student phone'
            elif not request.form['address']:
                error = 'You have to input the student address'
            else:
                g.execute("insert into student (id, name, gender, birthdate, phone, address) values ( %s, %s, %s, %s, %s, %s)", [
                    request.form['id'],
                    request.form['name'],
                    request.form['gender'],
                    request.form['birthdate'],
                    request.form['phone'],
                    request.form['address'],
                ])
                db.commit()
                return redirect(url_for('show_system'))
        return render_template('error.html', error=error)


@app.route('/data/delete', methods=['POST'])
def data_delete():
    if request.method == 'POST':
        if not request.form['id']:
            error = 'You have to input the student id'
        else:
            student = check_db('''select * from student where id = %s''',
                            [request.form['id']], one=True)
            if student is None:
                error = 'Invalid student id'
            else:
                g.execute('''delete from student where id=%s ''', [request.form['id']])
                db.commit()
                return redirect(url_for('show_system'))
    return render_template('error.html', error=error)


@app.route('/data/search', methods=['POST'])
def data_search():
    if request.method == 'POST':
        if not request.form['id']:
            error = 'You have to input the student id'
        elif not session.get('logged_in'):
            error = 'You have to log in'
        else:
            cur = g
            g.execute('''select * from student where id = %s''', [request.form['id']])
            datas = [dict(id=row[0], name=row[1], gender=row[2], birthdate=row[3], phone=row[4], address=row[5]) for row in
                           cur.fetchall()]
            return render_template('show_search.html', datas=datas)
    return render_template('error.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=23333)