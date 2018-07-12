import os

from flask import Blueprint, render_template, session, jsonify, request

from APP.models import User, House, Area, Facility, HouseImage

from utils import status_code
from utils.settings import UPLOAD_DIRS

house_blueprint = Blueprint('house', __name__)


# 我的房源页面
@house_blueprint.route('/myhouse/', methods=['GET'])
def myhouse():
    return render_template('myhouse.html')


# 我的房源页面
# 查看是否实名认证，
@house_blueprint.route('/auth_myhouse/', methods=['GET'])
def auth_myhouse():
    user = User.query.get(session['user_id'])
    if user.id_card:
        # 找出该用户下的房子
        houses = House.query.filter(House.user_id==user.id)
        hlist_list = []
        for house in houses:
            # 把每个房间的重点信息，放到列表中
            hlist_list.append(house.to_dict())

        return jsonify(code='200', hlist_list=hlist_list)

    else:
        return jsonify(status_code.MYHOUSE_USER_IS_NOT_AUTH)


# 发布新房源页面
@house_blueprint.route('/newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


# 发布新房源时需要使用的 房间设施参数 和 房间所在区域的参数
@house_blueprint.route('/area_facility/', methods=['GET'])
def area_facility():

    areas = Area.query.all()
    area_list = [area.to_dict() for area in areas]

    facilitys = Facility.query.all()
    facility_list = [facility.to_dict() for facility in facilitys]

    return jsonify(area_list=area_list, facility_list=facility_list)


# 发布新房源信息提交时访问的接口，
@house_blueprint.route('/newhouse/', methods=['POST'])
def user_newhouse():
    # 序列化提交过来， 得到的是一个对象， 把对象变成字典
    # 不序列化，得到的是一个字典，直接根据键取值
    house_dict = request.form.to_dict()
    # 复选框的name=facility， 多个复选框， 得到的是一个列表
    # 复选框根据name 可以取出value value是 设施的id
    # 多个值，使用getlist， 取出复选框的内容
    facility_ids = request.form.getlist('facility')

    # 把发布的方间信息，保存到数据库中
    house = House()
    house.user_id = session['user_id']
    house.title = house_dict.get('title')
    house.price = house_dict.get('price')
    house.area_id = house_dict.get('area_id')
    house.address = house_dict.get('address')
    house.root_count = house_dict.get('root_count')
    house.acreage = house_dict.get('acreage')
    house.unit = house_dict.get('unit')
    house.capacity = house_dict.get('capacity')
    house.beds = house_dict.get('beds')
    house.deposit = house_dict.get('deposit')
    house.min_days = house_dict.get('min_days')
    house.max_days = house_dict.get('max_days')

    # 如果接收到设施
    if facility_ids:
        # 过滤出设施id在列表中的的记录
        facilitys = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        # 构建多对多关系
        house.facilities = facilitys
    try:
        house.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify(code=status_code.OK, house_id=house.id)


# 发布新房源时，提交上传房子对应的图片时，访问的接口
@house_blueprint.route('/images/', methods=['POST'])
def newhouse_images():
    # $(this)指的是提交的操作， 提交操作提交的整个form表单
    # 包含标签， 根据input标签的属性name, 可以获取input标签的内容
    # 取出房间的图片
    images = request.files.get('house_image')
    # 取出房间的id
    house_id = request.form.get('house_id')

    # filename是图片的名字， 定义一个图片的保存路径
    url = os.path.join(UPLOAD_DIRS, images.filename)
    # 把图片保存到该路径中
    images.save(url)

    # 定义把图片保存到数据库中的路径
    image_url = os.path.join(os.path.join('/static', 'upload'), images.filename)

    # 专门用来保存房间图片的表格
    house_image = HouseImage()
    # 对应的房间号
    house_image.house_id = house_id
    # 对应的图片
    house_image.url = image_url

    try:
        house_image.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)

    # 房子在 设施、地区那次提交已经保存过了， 找到房子
    house = House.query.get(house_id)
    # 把上传的图片，也保存到与房子对应的表格中
    if not house.index_image_url:
        house.index_image_url = image_url
        try:
            house.add_update()
        except:
            return jsonify(status_code.DATABASE_ERROR)
    return jsonify(code=status_code.OK, image_url=image_url)



# 访问url中是添加id参数了， 但是可以不接收， 不用就完了
# 传入参数，是为了接收使用， 不使用也可以
@house_blueprint.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


# 点击房屋图片，展示房屋详情
@house_blueprint.route('/detail/<int:id>/', methods=['GET'])
def house_detail(id):
    # 根据url中传入的参数， 取出该房间
    house = House.query.get(id)
    # 多对多， 房间通过多对多关系，取出房间对应的设施
    facility_list = house.facilities
    # 房间的设施
    facility_dict_list = [facility.to_dict() for facility in facility_list]

    # 预定
    booking = 1
    # 如果用户登录
    if 'user_id' in session:
        # 房间的user_id
        house.user_id = session['user_id']

        booking = 0

    return jsonify(house=house.to_full_dict(),
                   facility_list=facility_dict_list,
                   booking=booking,
                   code=status_code.OK)


@house_blueprint.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')
