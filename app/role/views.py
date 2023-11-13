from flask import request
from app.role import role,role_api
from app import models
from app import db
from flask_restful import Resource
from app.utils.message import to_dict_msg


class Role(Resource):
    
    def get(self):
        role_list=[]
        try :
            roles = models.Role.query.all()
            role_list = [r.to_dict() for r in roles]
            return to_dict_msg(200,role_list,"獲取角色列表成功")
        except Exception as e:
            print(e)
            return to_dict_msg(20000)
        finally:
            db.session.close()
    def post(self):
        name = request.form.get('name')
        desc = request.form.get('desc')
        try:
            if name:
                role = models.Role(name=name,desc=desc)
                db.session.add(role)
                db.session.commit()
                db.session.close()
                return to_dict_msg(200,msg="新增角色成功!")
        except Exception as e:
            print(e)
            return to_dict_msg(20000)
        finally:
            db.session.close()
            
    def delete(self):
        try:
            id = int(request.form.get('id').strip())
            r = models.Role.query.get(id)
            # if r :
            db.session.delete(r)
            db.session.commit()
            return to_dict_msg(200,msg="刪除角色成功")
        except Exception:
            return to_dict_msg(20000)
        finally:
            db.session.close()
    def put(self):
        try:
            id = int(request.form.get('id').strip())
            name = request.form.get('name').strip() if request.form.get('name') else ""
            desc = request.form.get('desc').strip() if request.form.get('desc') else ""
            if name :
                r = models.Role.query.get(id)
                if r :
                    r.name=name
                    r.desc = desc
                    db.session.commit()
                    return to_dict_msg(200,msg="修改角色資訊成功!")
        except Exception as e:
            print(e)
            return to_dict_msg(20000)
role_api.add_resource(Role,'/role')

@role.route('/del_menu/<int:rid>/<int:mid>')
def del_menu(rid,mid):
    try:
        
        r = models.Role.query.get(rid)
        m = models.Menu.query.get(mid)
        if all([r,m]):
            if m in r.menus:
                r.menus.remove(m)
                if m.level==1:
                    for temp_m in m.children:
                        if temp_m in r.menus:
                            r.menus.remove(temp_m)
                db.session.commit()
                return to_dict_msg(200,"刪除權限成功")
            return to_dict_msg(10021)
        return to_dict_msg(10000)
    except Exception as e:
        print(e)
        return to_dict_msg(20000)

@role.route('/set_menu/<int:rid>',methods=['POST'])
def set_menu(rid):
    try:
        role = models.Role.query.get(rid)
        mids = request.form.get('mids')
        if role:
            role.menus=[]
            for m in mids.split(','):
                if m :
                    temp_menu = models.Menu.query.get(int(m))
                    if temp_menu:
                        role.menus.append(temp_menu)
            db.session.commit()
            return to_dict_msg(200,"權限分配成功")
        return to_dict_msg(10020)
    except Exception as e:
        print(e)
        return to_dict_msg(20000)