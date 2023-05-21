import math
import sqlite3
import time
import locale
from datetime import datetime
from pytz import timezone

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def create_db():
    """Вспомогательная функция для создания таблиц БД """
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addMenu(self, title, url):
        try:
            self.__cur.execute('INSERT INTO mainmenu VALUES (NULL, ?, ?)', (title, url))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления в БД', str(e))
            return False
        return True

    def delMenu(self, id=0):
        try:
            if id == 0:
                self.__cur.execute(f"DELETE FROM mainmenu")
            else:
                self.__cur.execute(f"DELETE FROM mainmenu WHERE id=={id}")
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка удаления из БД', str(e))
            return False
        return True

    def getMenu(self):
        try:
            sql = """SELECT *  FROM mainmenu"""
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Ошибка чтения из БД')
            return []

    def addPost(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES (NULL, ?, ?, ?)", (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления поста в БД", str(e))
            return False
        return True

    def getPostAnnoce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД" + str(e))
        return []

    def getPost(self, postid):
        try:
            self.__cur.execute(f"SELECT  title, text FROM posts WHERE id = {postid} LIMIT 1")
            res = self.__cur.fetchone()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД" + str(e))
        return (False, False)

    def addAnswer(self, id, title, text):
        try:
            sa_time = datetime.now(timezone('Europe/Moscow'))
            tm = sa_time.strftime('%d %B %Y %H:%M')
            self.__cur.execute("INSERT INTO answer VALUES (?, ?, ?, ?)", (id, title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления поста в БД", str(e))
            return False
        return True

    def getAnswerAnnoce(self, postid):
        try:
            self.__cur.execute(f"SELECT id, title, text , time FROM answer WHERE id = {postid}")
            res1 = self.__cur.fetchall()
            if res1: return res1
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД" + str(e))
        return []

    def getAnswer(self, postid):
        try:
            self.__cur.execute(f"SELECT  title, text FROM answer WHERE id = {postid} LIMIT 1")
            res1 = self.__cur.fetchone()
            if res1: return res1
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД" + str(e))
        return (False, False)


if __name__ == '__main__':
    from app import app, connect_db

    print(create_db.__doc__)
    db = connect_db()
    db = FDataBase(db)
    print(db)

    # for i in db.getMenu():
    # print(i['url'])

    # print(*db.getMenu())
    # print(db.delMenu())

    # print(db.addMenu('Главная', 'index'))

    create_db()
    print(db.addMenu('Задать вопрос', 'add_questions'))
    print(db.addMenu('Вопросы пользователей', 'all_questions'))
    # print(db.addAnswer('Задать вопрос', 'add_questions'))
    # print(db.getMenu())
