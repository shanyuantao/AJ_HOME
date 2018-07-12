from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 定义初始化app的方法
def init_ext(app):

    db.init_app(app=app)


# 定义数据库路径的方法
def get_database_uri(DATABASE):

    host = DATABASE.get('host')
    db = DATABASE.get('db')
    driver = DATABASE.get('driver')
    port = DATABASE.get('port')
    user = DATABASE.get('user')
    password = DATABASE.get('password')
    name = DATABASE.get('name')

    return '{}+{}://{}:{}@{}:{}/{}'.format(db, driver, user,
                                           password, host, port, name)

# 闭包
import functools
from flask import session, redirect

def is_login(views_fun):
    @functools.wraps(views_fun)
    def decorator():
        try:
            if 'user_id' in session:
                return views_fun()
            else:
                return redirect('/user/login/')
        except:
            return redirect('/user/login/')
    return decorator