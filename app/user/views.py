from app.user import user,user_api
from app import db
from app import models
from flask import request 
from flask_restful import Resource,reqparse
from app.utils.message import to_dict_msg
import re
from app.utils.token import login_required,verify_auth_token,generate_auth_token
@user.route("/")
def index():
    return "Hello user"

class User(Resource):
    def get(self):
        try:
            id = int(request.args.get('id').strip())
            usr = models.User.query.filter_by(id=id).first()
            if usr:
                return to_dict_msg(200,usr.to_dict(),"取得用戶成功!")
            else:
                return to_dict_msg(200,[],"沒有此用戶")
        except Exception as e:
            print(e)
            return to_dict_msg(10000)
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
            rid = int(request.form.get('role_id') if request.form.get('role_id') else 0)
            usr=models.User(name=name,password=pwd,nick_name=nick_name,phone=phone,email=email)
            db.session.add(usr)
            db.session.commit()
            return to_dict_msg(200)
        except Exception:
            return to_dict_msg(2000)
    def put(self):
        try:
            id = int(request.form.get('id').strip())
            email = request.form.get('email').strip() if request.form.get('email') else ''
            phone = request.form.get('phone').strip() if request.form.get('phone') else '' 
            rid = request.form.get('role_name').strip() if request.form.get('role_name') else ''
            usr = models.User.query.get(id)
            if usr:
                usr.email = email
                usr.phone = phone
                usr.rid = rid
                db.session.commit()
            return to_dict_msg(200,"修改用戶資訊成功")
        except Exception as e:
            print(e)
            return to_dict_msg(10000)
        
    def delete(self):
        try :
            id = int(request.form.get('id').strip())
            usr = models.User.query.get(id)
            if usr:
                db.session.delete(usr)
                db.session.commit()
                return to_dict_msg(200,"刪除用戶成功")
            else:
                return to_dict_msg(10019)
        except Exception as e:
            print(e)
            return to_dict_msg(2000)
            

class UserList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        # 这里的 location=['args']很关键，默认是['json']，适用前端请求的数据时JSON格式。
		# 因为当前是get请求，所以使用['args']接收前端请求的查询字符串参数
        parser.add_argument('name',type=str,location=['args'])
        parser.add_argument('pnum',type=int,location=['args'])
        parser.add_argument('psize',type=int,location=['args'])
        args = parser.parse_args()
        try:
            name = args.get('name')
            pnum = args.get('pnum') if args.get('pnum') else 1
            psize = args.get('psize') if args.get('psize') else 2
            
            if name:
                users_p = models.User.query.filter(models.User.name.like(f'%{name}%')).paginate(page=pnum,per_page=psize)
            else:
                users_p = models.User.query.paginate(page=pnum,per_page=psize)
            data = {
                'pnum':pnum,
                'totalPage':users_p.total,
                'users':[u.to_dict() for u in users_p.items]
            }
            return to_dict_msg(200,data,"取得用戶列表成功")
        except Exception as e:
            print(f'Exception: {e}')
            return to_dict_msg(10000)
        

user_api.add_resource(UserList,'/user_list')        
user_api.add_resource(User,'/user')

@user.route('/login',methods=['POST'])
@login_required
def login():
    name = request.form.get('name')
    pwd = request.form.get('pwd')
    
    if not all([name,pwd]):
        return to_dict_msg(10000)
    if len(name)>1:
        usr = models.User.query.filter_by(name=name).first()
        if usr:
            if usr.check_password(pwd):
                token = generate_auth_token(usr.id,1000000000)
                verify_auth_token(token)
                return to_dict_msg(200,data={'token':token})
    return  {'status':10001,'msg':'用户名或密碼錯誤'}
        
@user.route('/reset',methods=['GET'])
def reset():
    try:
        id =int(request.args.get('id'))
        usr = models.User.query.get(id)
        usr.password = '123'
        db.session.commit()
        return to_dict_msg(200,msg="重置密碼完成")
    except Exception as e:
        print(e)
        return to_dict_msg(20000)
        