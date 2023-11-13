from flask import request
from app.order import order,order_api
from app import models
from app import db
from flask_restful import Resource
from app.utils.message import to_dict_msg


@order.route('/order_list')
def get_order_list():
    id = request.args.get('id')
    if id :
        order = models.Order.query.get(id)
        if order:
            return to_dict_msg(200,order.to_dict(),"獲取訂單成功")
        else:
            return to_dict_msg(10022)
    orders = models.Order.query.all()
    
    return to_dict_msg(200,[o.to_dict() for o in orders],"獲取訂單列表成功")


# order_api.add_resource(Order,'/order')
@order.route('/express')
def get_express():
    try:
        oid = request.args.get('oid')
        if oid:
            exps = models.Express.query.filter(models.Express.oid == oid).order_by(models.Express.update_time.desc())
            return to_dict_msg(200,[e.to_dict() for e in exps])
        else:
            to_dict_msg(10000)
    except Exception as e:
        print(e)
        return to_dict_msg(20000)
