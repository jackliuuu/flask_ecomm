from flask import request
from app.category import category,category_api,attribute, attribute_api
from app import db ,models
from flask_restful import Resource
from app.utils.message import to_dict_msg
from sqlalchemy import func
# @category.route('/category_list')
# def test():
#     return 'test'


class Category(Resource):
    def get(self):
        try:
            cid = request.args.get('cid')
            c = models.Category.query.get(cid)
            if c:
                return to_dict_msg(200,c.to_dict(),"獲取商品分類成功")
            else:
                return to_dict_msg(10022)
        except Exception as e:
            print(e)
            return to_dict_msg(20000)
    def post(self):
        try:
            name = request.form.get('name') if request.form.get('name') else ''
            level = int(request.form.get('level')) if request.form.get('level') else None
            pid = int(request.form.get('id')) if request.form.get('id') else None
            if all([name,level]):
                if pid:
                    c = models.Category(name=name,level=level,pid=pid)
                else:
                    c = models.Category(name=name,level=level)
                db.session.add(c)
                db.session.commit()
                return to_dict_msg(200,"新增商品分類成功")
            return to_dict_msg(10000)
        except Exception as e:
            print(e)
            return to_dict_msg(20000)
    def put(self):
        try :
            cid = request.form.get('cid')
            name = request.form.get('name')
            c = models.Category.query.get(cid)
            if c:
                c.name = name
                db.session.commit()
                return to_dict_msg(200,"修改商品分類成功")
        except Exception as e:
            print(e)
            return to_dict_msg(20000)
category_api.add_resource(Category,'/category')


@category.route('/category_list',methods=['GET'])
def get_category_list():
    level = int(request.args.get('level')) if request.args.get('level') and int(request.args.get('level'))<=3 else 0
    pnum = int(request.args.get('pnum')) if request.args.get('pnum') else 0
    psize = int(request.args.get('psize')) if request.args.get('psize') else 0
    
    cate_list = []
    base_query = models.Category.query.filter(models.Category.level == 1)
    
    if all([pnum,psize]):
        categories =base_query.paginate(page=pnum,per_page=psize)
        if level :
            cate_list = get_tree(categories.items,level,True)
        else:
            cate_list = get_tree(categories.item,level,False)
        data = {
            'pnum':pnum,
            'psize':psize,
            'total':categories.total,
            'data':cate_list
            }
        return to_dict_msg(200,data,"獲取商品分類列表成功")
    else:
        categories = base_query.all()
        if level:
            cate_list = get_tree(categories,level,True)
        else:
            cate_list = get_tree(categories,level,False)
    return to_dict_msg(200,{'data':cate_list},"獲取商品分類列表成功")
            


def get_tree(info_list,flag,level):
    info_dict = []
    
    if info_list:
        for i in info_list:
            i_dict = i.to_dict()
            if flag:
                if i.level < level:
                    i_dict['children'] = get_tree(i.children,level,flag)
            else:
                if i.level!=3:
                    i_dict['children'] = get_tree(i.children, level, flag)   
            info_dict.append(i_dict)
    return info_dict

@category.route('/cate_group_level')
def get_cate_group_level():
    # 排除掉全部类，获取每一个等级里面存在多少个类
    group_data = db.session.query(models.Category.level,func.count(1).label('count')).group_by(models.Category.level).having(models.Category.level > 0).all()
    data = {
        'name': '数量',
        'xAxis':[f'{g[0]}级分类' for g in group_data],
        'series_data': [g[1] for g in group_data]
    }
    return to_dict_msg(200,data=data,msg='获取统计数据成功')

class Attribute(Resource):
    def get(self):
        try:
            id = request.args.get('id')
            attr = models.Attribute.query.get(id)
            if attr:
                return to_dict_msg(200,attr.to_dict(),"獲取分類參數成功")
            else:
                return to_dict_msg(10022)
        except Exception as e:
            print(e)
            return to_dict_msg(20000)
    def post(self):
        name = request.form.get('name')
        cid = request.form.get('cid')
        val = request.form.get('val')
        _type = request.form.get('_type')
        if all([name,cid,_type]):
            if val:
                attr = models.Attribute(name=name,cid=int(cid),_type=_type,val=val)
            else:
                attr = models.Attribute(name=name,cid=int(cid),_type=_type)
            db.session.add(attr)
            db.session.commit()
            return to_dict_msg(200,"新增商品分類數據成功")
        else:
            return to_dict_msg(10000)
    def put(self):
        try:
            id =request.form.get('id')
            val = request.form.get('val')
            name = request.form.get('name')
            cid = int(request.form.get('cid')) if request.form.get('cid') else 0
            if all([id,cid,name]):
                attr = models.Attribute.query.get(id)
                if attr:
                    attr.name = name
                    attr.val = val
                    attr.cid = cid
                    db.session.commit()
                    return to_dict_msg(200,msg="數據更新成功")
                else:
                    return to_dict_msg(10022)
            else:
                return to_dict_msg(10000)
        except Exception as e:
            print(e)
            return to_dict_msg(20000)
    def delete(self):
        try:
            id = request.form.get('id')
            attr = models.Attribute.query.get(id)
            if attr:
                db.session.delete(attr)
                db.session.commit()
                return to_dict_msg(200,"成功刪除分類參數")
            else:
                return to_dict_msg(10022)
        except Exception as e:
            print(e)
            return to_dict_msg(20000)
attribute_api.add_resource(Attribute,'/attribute')

@attribute.route('/attr_list')
def get_attr_list():
    cid = request.args.get('cid')
    _type = request.args.get('_type')
    if all([cid,_type]):
        cate = models.Category.query.get(cid)
        if cate:
            if _type == "static":
                attr_list = [a.to_dict() for a in cate.attrs if a._type == "static"]
            else:
                attr_list = [a.to_dict() for a in cate.attrs if a._type == "dynamic"]
            return to_dict_msg(200,attr_list,msg="獲取分類屬性列表成功")
        else:
            return to_dict_msg(10022)
    else:
        return to_dict_msg(10000)