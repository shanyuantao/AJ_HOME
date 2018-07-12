import re
import os


from flask import Blueprint, render_template, request, \
    jsonify, session

from utils.functions import db, is_login
from utils import status_code

from APP.models import User

# 注册路由
from utils.settings import UPLOAD_DIRS

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/')
def hello_user():
    return '欢迎'


# 创建数据库
@user_blueprint.route('/createdb/')
def create_db():
    db.create_all()
    return '创建数据库成功'


# 注册页面
@user_blueprint.route('/register/', methods=['GET'])
def register():

    return render_template('register.html')


# 提交注册页面
@user_blueprint.route('/register/', methods=['POST'])
def sure_register():
    # 取出提交页面中的内容，是个字典
    register_dict = request.form
    mobile = register_dict.get('mobile')
    password = register_dict.get('password')
    password2 = register_dict.get('password')

    # 填写信息不全
    if not all([mobile, password, password2]):
        return jsonify(status_code.USER_REGISTER_PARAMS_ERROR)

    # 不符合号码规则
    if not re.match(r'^1[24578]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTE_MOBILE_ERROR)

    # 用户是否已注册
    if User.query.filter(User.phone == mobile).count():
        return jsonify(status_code.USER_REGISTE_MOBILE_IS_EXISTS)

    # 两次输入的密码不相等
    if password != password2:
        return jsonify(status_code.USER_REGISTER_PASSWORD_IS_ERROR)

    # 创建字段
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = password

    try:
        # 保存字段
        user.add_update()
        return jsonify(status_code.SUCCESS)

    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)


# 登录页面
@user_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


# 提交登录页面
@user_blueprint.route('/login/', methods=['POST'])
def user_login():
    user_dict = request.form
    mobile = user_dict.get('mobile')
    password = user_dict.get('password')

    if not all([mobile, password]):
        return jsonify(status_code.PARAMS_ERROR)

    if not re.match(r'^1[34578]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTE_MOBILE_ERROR)

    user = User.query.filter(User.phone == mobile).first()
    # 如果用户已经注册过
    if user:
        # 如果输入的密码和注册的密码相同
        if user.check_pwd(password):
            # 把用户的id存放到，session中对应的键为user_id
            session['user_id'] = user.id
            return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.USER_LOGIN_PASSWORD_IS_ERROR)
    else:
        return jsonify(status_code.USER_LOGIN_IS_NOT_EXSITS)


@user_blueprint.route('/my/', methods=['GET'])
def my():
    return render_template('my.html')


# 得到用户的信息， 用来填充页面
@user_blueprint.route('/user/', methods=['GET'])
def get_user_profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    # 返回对象的名字， 头像， 电话， 对象的 id， 返回状态码200
    return jsonify(user=user.to_basic_dict(), code=200)


# 修改信息的页面
@user_blueprint.route('/profile/', methods=['GET'])
def profile():
    return render_template('profile.html')


# 修改头像用户名的方法
@user_blueprint.route('/user/', methods=['PUT'])
def user_profile():
    # 得到是个字典，相当于request.POST.get('avatar')
    user_dict = request.form
    file_dict = request.files
    # 如果接收到图片
    if 'avatar' in file_dict:
        # 根据键取出图片
        f1 = file_dict['avatar']
        # 判断图片的类型
        if not re.match(r'^image/.*$', f1.mimetype):
            return jsonify(status_code.USER_UPLOAD_IMAGE_IS_ERROR)
        # 定义一个url
        url = os.path.join(UPLOAD_DIRS, f1.filename)
        # f1是个图片，该图片可以保存路径
        f1.save(url)
        # 取出登录的用户
        user = User.query.filter(User.id == session['user_id']).first()
        # 定义一个url, 这是一个绝对路径，就去static下去找
        image_url = os.path.join('/static/upload', f1.filename)
        # 把图片的路径保存到数据库中
        user.avatar = image_url
        try:
            # 更改已有记录需要保存
            user.add_update()
            # 返回url
            return jsonify(code=status_code.OK, url=image_url)
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)

    elif 'name' in user_dict:
        name = user_dict.get('name')
        if User.query.filter(User.name == name).count():
            return jsonify(status_code.USER_UPDATE_USERNAME_IS_EXISTS)

        # 如果名字不在表格中， 替换用户名字段的名字
        user = User.query.get(session['user_id'])
        user.name = name

        try:
            # 更改已有字段要保存
            user.add_update()
            return jsonify(status_code.SUCCESS)
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)
    else:
        return jsonify(status_code.PARAMS_ERROR)


# 实名认证
@user_blueprint.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


# 实名认证页面，保存认证信息， 隐藏提交按钮
@user_blueprint.route('/auths/', methods=['PUT'])
@is_login
def user_auth():
    user_dict = request.form

    id_name = user_dict.get('id_name')
    id_card = user_dict.get('id_card')

    if not re.match(r'[1-9]\d{17}$', id_card):
        return jsonify(status_code.USER_AUTH_IDCARD_IS_ERROR)

    if not re.match(r'^[1-9]\d{17}$', id_card):
        return jsonify(status_code.USER_AUTH_IDCARD_IS_ERROR)

    try:
        user = User.query.get(session['user_id'])
        user.id_card = id_card
        user.id_name = id_name

        user.id_name = id_name
        user.add_update()
        return jsonify(status_code.SUCCESS)

    except:

        return jsonify(status_code.DATABASE_ERROR)


# js后台访问的方法， 如果已经实名认证， 则获取认证信息， 填充页面
# 其他js则弹出警告， 让实名认证
@user_blueprint.route('/auths/', methods=['GET'])
@is_login
def get_user_auth():
    user = User.query.get(session['user_id'])
    if user.id_name:
        return jsonify(code=status_code.OK,
                       id_name=user.id_name,
                       id_card=user.id_card)

    else:
        return jsonify(code=status_code.PARAMS_ERROR)


@user_blueprint.route('/logout/')
def user_logout():
    # 退出登录清除session
    session.clear()
    return jsonify(status_code.SUCCESS)