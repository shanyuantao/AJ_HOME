import os

from utils.functions import get_database_uri

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#设置静态文件的路径
static_dir = os.path.join(BASE_DIR, 'static')

# 模板路径设置
templates_dir = os.path.join(BASE_DIR, 'templates')

DATABASE = {
    'db': 'mysql',
    'driver': 'pymysql',
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': '123123',
    'name': 'aj_db'
}
# 设置mysql数据哭的路径
SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)
# 设置文件上传的路径
UPLOAD_DIRS = os.path.join(os.path.join(BASE_DIR, 'static'), 'upload')

