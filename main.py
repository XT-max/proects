
import datetime
import os
import sqlite3

from flask import Flask, render_template, flash, request, abort, g

from config import Config
from fdatabase import FDataBase

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fdb.db')))
app.permanent_session_lifetime = datetime.timedelta(seconds=60)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """Соединение с БД, если оно еще не установленно"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/add_questions', methods=['POST', 'GET'])
def add_questions():
    db = get_db()
    database = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['name']) <= 3 and len(request.form['name']) <= 75:
            flash('Вопрос должно быть не меньше 3 и не больше 75 символов.', category='error')
        if len(request.form['post']) <= 2 and len(request.form['post']) <= 250:
            flash('Описание вопроса должно быть не меньше 2 и не больше 250 символов.', category='error')
        elif 3 <= len(request.form['name']) <= 75 and 2 <= len(request.form['post']) <= 250:
            res = database.addPost(request.form['name'], request.form['post'])
            if res:
                flash('Вопрос опубликован', category='success')


    return render_template('add_questions.html', title='Добавить статью', menu=database.getMenu())



@app.route('/all_questions', methods=['POST', 'GET'])
def all_questions():  # put application's code here
    db = get_db()
    database = FDataBase(db)
    return render_template('all_questions.html', title='Cписок постов', menu=database.getMenu()
                           ,posts=database.getPostAnnoce())




@app.route('/posts/<int:id_post>', methods=['POST', 'GET'])
def showPost(id_post):  # put application's code here

    db = get_db()
    database = FDataBase(db)
    title, aticle = database.getPost(id_post)
    answer = database.getAnswer(id_post)
    for i in database.getAnswerAnnoce(id_post):
        print(i)
    if request.method == 'POST':
        if len(request.form['us']) <= 3 and len(request.form['us']) <= 15:
            flash('Имя должно быть не меньше 3 и не больше 15 символов.', category='error')
        if len(request.form['vp']) <= 2 and len(request.form['vp']) <= 250:
            flash('Вопрос должен быть не меньше 2 и не больше 250 символов.', category='error')
        elif 3 <= len(request.form['us']) <= 15 and 2 <= len(request.form['vp']) <= 250:
            res1 = database.addAnswer(id_post, request.form['us'], request.form['vp'])

            if res1:
                flash('Ответ опубликован', category='success')

    if not title:
        abort(404)
    return render_template('aticle.html', title='title', menu=database.getMenu(), post=aticle, post1=answer
                           ,otv=database.getAnswerAnnoce(id_post))




@app.route('/')
def index():
    db = get_db()
    database = FDataBase(db)
    return render_template('main.html', title='1', menu=database.getMenu())


if __name__ == '__main__':
    app.run(debug=True)
