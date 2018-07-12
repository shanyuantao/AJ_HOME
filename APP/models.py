from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from utils.functions import db


class BaseModel(object):

    create_time = db.Column(db.DATETIME, default=datetime.now())
    update_time = db.Column(db.DATETIME, default=datetime.now(),
                            onupdate=datetime.now())

    def add_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(BaseModel, db.Model):

    __tablename__ = 'ihome_user'
    # 用户的id
    id = db.Column(db.INTEGER, primary_key=True)
    # 手机号
    phone = db.Column(db.String(11), unique=True)
    # 加密后的密码
    pwd_hash = db.Column(db.String(200))
    # 用户的名字
    name = db.Column(db.String(30), unique=True)
    # 头像
    avatar = db.Column(db.String(100))
    # 实名认证的姓名
    id_name = db.Column(db.String(30))
    # 实名认证的身份证号
    id_card = db.Column(db.String(18), unique=True)
    # 关联 房子
    houses = db.relationship('House', backref='user')
    # 关联 订单
    orders = db.relationship('Order', backref='user')

    # 访问器
    @property
    def password(self):
        return ''

    # 修改器
    @password.setter
    def password(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    # 检查 密码是否相等
    def check_pwd(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)

    # 字典 用户id、用户头像、用户姓名、用户手机号
    def to_basic_dict(self):
        return {
            'id': self.id,
            'avatar': self.avatar if self.avatar else '',
            'name': self.name,
            'phone': self.phone
        }


# 房间 和 设施是多对多关系  多对多关系专门使用一个表格管理，表格名称， 两个外键
ihome_house_facility = db.Table(
    'ihome_house_facility',
    db.Column('house_id', db.Integer, db.ForeignKey('ihome_house.id'), primary_key=True),
    db.Column('facility_id', db.Integer, db.ForeignKey('ihome_facility.id'), primary_key=True)
)


class House(BaseModel, db.Model):

    __tablename__ = 'ihome_house'
    # 房间的id
    id = db.Column(db.Integer, primary_key=True)
    # 该房间用户的id，外键关联用户的 id
    user_id = db.Column(db.Integer, db.ForeignKey('ihome_user.id'), nullable=False)
    # 该房间所在区域的id， 外键关联房间所在区域的 id
    area_id = db.Column(db.Integer, db.ForeignKey('ihome_area.id'), nullable=False)
    # 该房间的标题
    title = db.Column(db.String(64), nullable=False)
    # 该房间的价格
    price = db.Column(db.Integer, default=0)
    # 该房间所在的详细地址
    address = db.Column(db.String(512), default="")
    # 房间的数量
    room_count = db.Column(db.Integer, default=1)
    # 该房间的面积
    acreage = db.Column(db.Integer, default=0)
    # 房间类型.几室几厅
    unit = db.Column(db.String(32), default="")
    # 房间的容量，可以容纳几人
    capacity = db.Column(db.Integer, default=1)
    # 房间的床的信息
    beds = db.Column(db.String(64), default="")
    # 需要交纳的押金
    deposit = db.Column(db.Integer, default=0)
    # 最少入住的天数
    min_days = db.Column(db.Integer, default=0)
    # 最多入住的天数
    max_days = db.Column(db.Integer, default=0)

    order_count = db.Column(db.Integer, default=0)

    index_image_url = db.Column(db.String(256), default="")
    # 房间的设施，与设施是多对多关系
    facilities = db.relationship('Facility', secondary=ihome_house_facility)
    # 房间的图片， 与房间是一对多关系
    images = db.relationship('HouseImage')
    # 订单
    orders = db.relationship('Order', backref='house')

    def to_dict(self):
        return {
            'id': self.id,

            'title': self.title,

            'image': self.index_image_url if self.index_image_url else '',

            'area': self.area.name,

            'price': self.price,

            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),

            'room': self.room_count,

            'order_count': self.order_count,

            'address': self.address
        }

    def to_full_dict(self):
        return {
            'id': self.id,
            'user_avatar': self.user.avatar if self.user.avatar else '',
            'user_name': self.user.name,
            'title': self.title,
            'price': self.price,
            'address': self.area.name + self.address,
            'room_count': self.room_count,
            'acreage': self.acreage,
            'unit': self.unit,
            'capacity': self.capacity,
            'beds': self.beds,
            'deposit': self.deposit,
            'min_days': self.min_days,
            'max_days': self.max_days,
            'order_count': self.order_count,
            'images': [image.url for image in self.images],
            'facilities': [facility.to_dict() for facility in self.facilities],

        }


class HouseImage(BaseModel, db.Model):

    __tablename__ = 'ihome_house_image'

    id = db.Column(db.Integer, primary_key=True)
    # 外键关联房间的id
    house_id = db.Column(db.Integer, db.ForeignKey('ihome_house.id'), nullable=False)
    # 图片
    url = db.Column(db.String(256), nullable=False)


class Facility(BaseModel, db.Model):

    __tablename__ = 'ihome_facility'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    css = db.Column(db.String(30), nullable=True)

    # 把对象初始化下面的字典模式
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'css': self.css
        }

    def to_house_dict(self):
        return {'id': self.id}


class Area(BaseModel, db.Model):

    __tablename__ = 'ihome_area'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    houses = db.relationship('House', backref='area')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Order(BaseModel, db.Model):

    __tablename__ = 'ihome_order'

    id = db.Column(db.Integer, primary_key=True)
    # 外键关联用户， 一个用户对应多个订单
    user_id = db.Column(db.Integer, db.ForeignKey('ihome_user.id'), nullable=False)
    # 一个房子对应多个订单
    house_id = db.Column(db.Integer, db.ForeignKey('ihome_house.id'), nullable=False)
    # 订单的创建时间
    begin_date = db.Column(db.DateTime, nullable=False)
    # 订单的结束时间
    end_date = db.Column(db.DateTime, nullable=False)
    # 订单生效的天数
    days = db.Column(db.Integer, nullable=False)
    # 房间的价格
    house_price = db.Column(db.Integer, nullable=False)
    # 房间的数量
    amount = db.Column(db.Integer, nullable=False)
    # 订单的状态，使用了枚举法, index 等于 true 意思是 默认开启了下标索引， WAIT_ACCEPT相当于0， 可以使用时可以用0代替
    status = db.Column(
        db.Enum(
            # 待接单
            'WAIT_ACCEPT',
            # 待支付
            'WAIT_PAYMENT',
            # 已支付
            'PAID',
            # 待评价
            'WAIT_COMMENT',
            # 已完成
            'COMPLETE',
            # 已取消
            'CANCELED',
            # 已拒单
            'REJECTED'
        ),
        default='WAIT_ACCEPT', index=True
    )
    # 订单评价
    comment = db.Column(db.Text)

    # 把订单对象初始化如下的字典形式
    def to_dict(self):
        return {
            'order_id': self.id,
            'house_title': self.house.title,
            'image': self.house.index_image_url if self.house.index_image_url else '',
            'create_date': self.create_time.strftime('%Y-%m-%d'),
            'begin_date': self.begin_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'amount': self.amount,
            'days': self.days,
            'status': self.status,
            'comment': self.comment
        }
