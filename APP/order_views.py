from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session

from APP.models import House, Order
from utils import status_code

order_blueprint = Blueprint('order', __name__)


# 点击即刻预定时访问
@order_blueprint.route('/', methods=['POST'])
def order():
    # 接收提交时传入的参数
    order_dict = request.form
    # 取出预定的房间id
    house_id = order_dict.get('house_id')

    # 转换时间的格式
    start_time = datetime.strptime(order_dict.get('start_time'), '%Y-%m-%d')
    end_time = datetime.strptime(order_dict.get('end_time'), '%Y-%m-%d')

    if not all([house_id, start_time, end_time]):
        return jsonify(status_code.PARAMS_ERROR)

    if start_time > end_time:
        return jsonify(status_code.ORDER_START_TIME_GT_END_TIME)

    # 取出房间
    house = House.query.get(house_id)

    # 创建订单
    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_time
    order.end_date = end_time
    order.house_price = house.price

    order.days = (end_time - start_time).days + 1

    order.amount = order.days * order.house_price

    try:
        order.add_update()
        return jsonify(code=status_code.OK)

    except:
        return jsonify(status_code.DATABASE_ERROR)


# 点击提交订单时访问
@order_blueprint.route('/order/', methods=['GET'])
def orders():

    return render_template('orders.html')



# 我的订单页面访问的接口
@order_blueprint.route('/allorders/', methods=['GET'])
def all_orders():

    user_id = session['user_id']
    order_list = Order.query.filter(Order.user_id==user_id)
    order_list2 = [order.to_dict() for order in order_list]
    return jsonify(code=status_code.OK, order_list=order_list2)


# 客户订单页面
@order_blueprint.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


# 客户订单页面加载时访问的页面
@order_blueprint.route('/fd/', methods=['GET'])
def lorders_fd():

    # 找出用户下的房子
    houses = House.query.filter(House.user_id==session['user_id'])
    # 取出房子的id
    houses_ids = [house.id for house in houses]

    # 根据房子的id找订单， 订单和房子是关联的
    orders = Order.query.filter(Order.house_id.in_(houses_ids)).order_by(Order.id.desc())
    # 取出各订单
    olist = [order.to_dict() for order in orders]

    # # 第二种方式
    # house = House.query.filter(House.user_id == session['user_id'])
    # order_list = []
    # for house in house:
    #     orders = house.orders
    #
    # olist = [order.to_dict() for order in orders]


    return jsonify(olist=olist, code=status_code.OK)


@order_blueprint.route('/order/<int:id>/', methods=['PUT'])
def orders_status(id):

    status = request.form.get('status')

    order = Order.query.get('status')

    order.status = status

    if status == 'REJECTED':

        comment = request.form.get('comment')
        order.comment = comment

    try:
        order.add_update()

    except:
        return jsonify(status_code.DATABASE_ERROR)

    return jsonify(code=status_code.OK)