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
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    level = db.Column(db.Integer)
    path = db.Column(db.String(32))
    pid = db.Column(db.Integer,db.ForeignKey('t_menu.id'))
    children = db.relationship('Menu')
    roles = db.relationship('Role',secondary=trm,back_populates='menus')
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'level':self.level,
            'path':self.path,
            'pid':self.pid,
            # 'children':self.get_child_list()
        }
    def get_child_list(self):
        obj_child =self.children
        data= []
        for obj in obj_child:
            data.append(obj.to_dict)
        return data

class Role(db.Model):
    __tablename__= 't_role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True,nullable=True)
    desc = db.Column(db.String(32))
    users = db.relationship('User', backref='Role')
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
        for m in self.menus:
            # 一共就两级，二级的应该放在一级的当作children输出
            if m.level == 1:
                first_dict = m.to_dict()
                first_dict['children'] = []
                for s in self.menus:
                    # 只有二级才需要加入到children，并判断是否为关联关系
                    if s.level == 2 and s.pid == m.id:
                        first_dict['children'].append(s.to_dict())
                menu_list.append(first_dict)
        return menu_list

