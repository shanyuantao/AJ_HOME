from flask import Flask

from APP.house_views import house_blueprint
from APP.order_views import order_blueprint
from APP.user_views import user_blueprint
from utils.functions import init_ext
from utils.settings import static_dir, templates_dir


def create_app(config):
    # 定义app
    app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)

    # 定义app的配置
    app.config.from_object(config)
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')
    app.register_blueprint(blueprint=order_blueprint, url_prefix='/order')

    # 使用SQLAlchemy初始化app
    init_ext(app)

    return app