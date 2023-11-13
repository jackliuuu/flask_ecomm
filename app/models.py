from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy

class BaseModel:
    # 紀錄創建的時間
    create_time = db.Column(db.DateTime,default=datetime.now)
    # 紀錄修改的時間
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate = datetime.now)

trm = db.Table('t_role_menu',
               db.Column('rid',db.Integer,db.ForeignKey('t_role.id')),
               db.Column('mid',db.Integer,db.ForeignKey('t_menu.id'))
               )
class User(db.Model,BaseModel):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    pwd = db.Column(db.String(256))
    nick_name = db.Column(db.String(32))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(32))
    rid = db.Column(db.Integer, db.ForeignKey('t_role.id'))


    @property
    def password(self):
        return self.pwd
    
    @password.setter
    def password(self,t_pwd):
        self.pwd=generate_password_hash(t_pwd)
        
    def check_password(self,t_pwd):
        return check_password_hash(self.pwd,t_pwd)
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'nick_name':self.nick_name,
            'phone':self.phone,
            'email': self.email,
            'role_name': self.role.name if self.role else ''
        }
    
class Menu(db.Model):
    __tablename__ = 't_menu'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32),unique = True, nullable = False)
    level = db.Column(db.Integer)
    path = db.Column(db.String(32))
    # pid = db.Column(db.Integer)
    pid = db.Column(db.Integer, db.ForeignKey('t_menu.id'))
    # 建立一个自连接的数据，用于做子表
    children = db.relationship('Menu')
    roles = db.relationship('Role', secondary = trm)


    # 由于前端的接收需要给出json数据，不可以直接去获取，所以得单独返回
    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'level':self.level,
            'path':self.path,
            'pid':self.pid,
            # 子表中的内容需要单独返回，可以做一个递归或者循环
            # 'children': self.get_child_list()
        }
    def get_child_list(self):
        obj_child = self.children
        data = []
        for o in obj_child:
            data.append(o.to_dict())
        return data


# 角色管理
class Role(db.Model):
    __tablename__ = 't_role'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique=True, nullable = True)
    desc = db.Column(db.String(32))
    # backref反向关联，方便子表查询主表数据
    users = db.relationship('User', backref='role')
    menus = db.relationship('Menu', secondary = trm)

    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'desc':self.desc,
            'menu': self.get_menu_dict()
        }
    
    def get_menu_dict(self):
        menu_list = []
        menus = sorted(self.menus,key = lambda temp:temp.id)
        for m in menus:
            # 一共就两级，二级的应该放在一级的当作children输出
            if m.level == 1:
                first_dict = m.to_dict()
                first_dict['children'] = []
                for s in menus:
                    # 只有二级才需要加入到children，并判断是否为关联关系
                    if s.level == 2 and s.pid == m.id:
                        first_dict['children'].append(s.to_dict())
                menu_list.append(first_dict)
        return menu_list


class Category(db.Model):
    __tablename__ = 't_category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),nullable=True)
    level = db.Column(db.Integer)
    attrs = db.relationship('Attribute', backref='category')
    pid = db.Column(db.Integer,db.ForeignKey('t_category.id'))
    children = db.relationship('Category')

    def to_dict(self):
        return {
            'id':self.id,
            'name' : self.name,
            'level': self.level,
            'pid': self.pid
        }

class Attribute(db.Model):
    __tablename__= "t_attribute"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    val = db.Column(db.String(255))
    cid = db.Column(db.Integer, db.ForeignKey('t_category.id')) # 外键关联商品分类表
    _type = db.Column(db.Enum('static', 'dynamic'))

    
    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'val':self.val,
            'cid':self.cid,
            '_type':self._type
        }

class Goods(db.Model):
    __tablename__ = "t_goods"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512)) # 商品名稱
    price = db.Column(db.Float)
    number = db.Column(db.Integer) # 商品庫存
    introduce = db.Column(db.Text) # 商品介绍
    big_log = db.Column(db.String(256)) # 商品大照片
    small_log = db.Column(db.String(256)) # 商品小照片
    state = db.Column(db.Integer) # 0未通過 1審核中 2已審核
    is_promote = db.Column(db.Integer) # 是否促銷
    hot_number = db.Column(db.Integer) # 促銷數量
    weight = db.Column(db.Integer) # 權重比例，用於促銷
    cid_one = db.Column(db.Integer, db.ForeignKey('t_category.id'))
    cid_two = db.Column(db.Integer, db.ForeignKey('t_category.id'))
    cid_three = db.Column(db.Integer, db.ForeignKey('t_category.id')) # 屬於哪個分類，有三級列表

    # 外键的方式与Category表建立关系
    category = db.relationship('Category', foreign_keys=[cid_three])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'number': self.number,
            'introduce': self.introduce,
            'big_log': self.big_log,
            'small_log': self.small_log,
            'state': self.state,
            'is_promte': self.is_promte,
            'hot_number': self.hot_number,
            'weight': self.weight,
            'cid_one': self.cid_one,
            'cid_two': self.cid_two,
            'cid_three': self.cid_three,
            'attrs': [a.to_dict() for a in self.category.attrs]
        }
        
class Picture(db.Model):
    __tablename__ = "t_picture"
    id = db.Column(db.Integer,primary_key=True)
    path = db.Column(db.String(512))
    gid = db.Column(db.Integer,db.ForeignKey('t_goods.id'))

class GoodsAttr(db.Model):
    __tablename__ = 't_goods_attr'
    gid = db.Column(db.Integer, db.ForeignKey('t_goods.id'), primary_key=True)
    aid = db.Column(db.Integer, db.ForeignKey('t_attribute.id'), primary_key=True)
    val = db.Column(db.String(512))
    _type = db.Column(db.String(8))
    
class Order(db.Model,BaseModel):
    __tablename__ = "t_order"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    price = db.Column(db.Float)
    number = db.Column(db.Integer)
    pay_status = db.Column(db.Integer) # 支付状态： 0未支付，1支付
    is_send = db.Column(db.Integer) # 是否发货
    fapiao_title = db.Column(db.String(32))
    fapiao_company = db.Column(db.String(128))
    fapiao_content = db.Column(db.String(521))
    addrs =db.Column(db.String(512))

    # 关联订单详情表与物流信息表
    user = db.relationship('User', foreign_keys=[uid])
    order_detail = db.relationship('OrderDetail', backref = 'order')
    express = db.relationship('Express', backref = 'order')
    
    def to_dict(self):
        return {
            'id':self.id,
            'uid':self.uid,
            'uname':self.user.nick_name,
            'price':self.price,
            'number':self.number,
            'pay_status':self.pay_status,
            'is_send':self.is_send,
            'fapiao_title':self.fapiao_title,
            'fapiao_company':self.fapiao_company,
            'fapiao_content':self.fapiao_content,
            'addrs':self.addrs
        }

    
    

# 订单详情表
class OrderDetail(db.Model):
    __tablename__ = 't_order_detail'
    gid = db.Column(db.Integer, db.ForeignKey('t_goods.id'), primary_key=True)
    oid = db.Column(db.Integer, db.ForeignKey('t_order.id'), primary_key=True)
    number = db.Column(db.Integer)
    price = db.Column(db.Float)
    total_price = db.Column(db.Float)



# 物流信息表
class Express(db.Model):
    __tablename__ = 't_express'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(64))
    update_time = db.Column(db.String(32))
    oid = db.Column(db.Integer, db.ForeignKey('t_order.id'))
    
    
    def to_dict(self):
        return{
            'id':self.id,
            'content':self.content,
            'udpate_time':self.update_time,
            'oid':self.oid
        }