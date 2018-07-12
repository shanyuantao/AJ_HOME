import redis

from utils.settings import SQLALCHEMY_DATABASE_URI


class Config:

    # 定义数据库路径
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 秘钥 可以随意写
    SECRET_KEY = 'secret_key'
    # SESSION使用的数据库类型
    SESSION_TYPE = 'redis'
    # SESSION连接数据库配置
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379')
    # 给redis数据库中生成的session条目，添加前缀，便于区分
    SESSION_KEY_PREFIX = 's_aj_'