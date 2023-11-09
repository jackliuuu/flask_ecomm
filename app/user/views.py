from app.user import user,user_api
from app import db
from app import models
from flask import request 
from flask_restful import Resource
from app.utils.message import to_dict_msg
from app.utils.token import generate_auth_token
import re
@user.route("/")
def index():
    return "Hello user"

class User(Resource):
    def get(self):
        pass
    def post(self):

        name = request.form.get('name')
        pwd=request.form.get('pwd')
        real_pwd = request.form.get('real_pwd')
        nick_name = request.form.get('nick_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
 
        if not all([name,pwd,real_pwd]):
            return to_dict_msg(10000)
        if len(name)<2:
            return to_dict_msg(10001)
        if len(pwd)<2:
            return to_dict_msg(10012)
        if pwd!=real_pwd:
            return to_dict_msg(10013)
        if not re.match(r'^09\d{8}$',phone):
            return to_dict_msg(10014)
        if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$',email):
            return to_dict_msg(10015)

        try:
            usr=models.User(name=name,pwd=pwd,nick_name=nick_name,phone=phone,email=email)
            db.session.add(usr)
            db.session.commit()
            return to_dict_msg(200)
        except Exception:
            return to_dict_msg(2000)
        
user_api.add_resource(User,'/user')

@user.route('/login',methods=['POST'])
def login():
    name = request.form.get('name')
    pwd = request.form.get('pwd')
    
    if not all([name,pwd]):
        return to_dict_msg(10000)
    if len(name)>1:
        usr = models.User.query.filter_by(name=name).first()
        if usr:
           
            if usr.check_password(pwd):
                print("_________A__________")
                token = generate_auth_token(usr.id,1000)
                return to_dict_msg(200,data={'token':token})
    return  {'status':10001,'msg':'用户名或密碼錯誤'}
        
        
