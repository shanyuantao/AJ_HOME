from flask_script import Manager
from utils.config import Config
from utils.app import create_app


app = create_app(Config)
manager = Manager(app=app)

if __name__ == '__main__':

    manager.run()

