from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class BaseModel:
    # 紀錄創建的時間
    create_time = db.Column(db.DateTime,default=datetime.now)
    # 紀錄修改的時間
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate = datetime.now)


class User(db.Model,BaseModel):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    pwd = db.Column(db.String(128))
    nick_name = db.Column(db.String(32))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(32))


    @property
    def password(self):
        return self.pwd
    
    @password.setter
    def password(self,t_pwd):
        self.pwd=generate_password_hash(t_pwd)
        
    def check_password(self,t_pwd):
        return check_password_hash(self.pwd,t_pwd)