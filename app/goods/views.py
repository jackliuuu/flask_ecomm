# flask_shop/goods/view.py
from flask import request
from app.goods import goods,goods_api
from app import models,db
from flask_restful import Resource
from app.utils.message import to_dict_msg
from app import Config
import hashlib
from time import time
class Goods(Resource):
    def delete(self):
        id = request.form.get('id')
        goods = models.Goods.query.get(id)
        if goods:
            db.session.delete(goods)
            db.session.commit()
            return to_dict_msg(200,msg="刪除商品成功")
        else:
            return to_dict_msg(10022) 


@goods.route('/goods_list')
def get_goods_list():
    try:
        name = request.args.get('name')
        if name :
            goods = models.Goods.query.filter(models.Goods.name.like(f'%{name}%'))
        else:
            goods = models.Goods.query.all()
        good_list = [gds.to_dict() for gds in goods]
        return to_dict_msg(200,good_list,msg="獲取商品列表成功")
    except Exception as e:
        print(e)
        return to_dict_msg(10000)
@goods.route('/upload_img',methods=['POST'])
def upload_img():
    img_file = request.files.get('file')
    if not img_file:
        return to_dict_msg(10023)
    if allowed_img(img_file.filename):
        folder = Config.SERVER_IMG_UPLOADS
        end_prefix = img_file.filename.rsplit('.',1)[1]
        file_name = md5_file()
        img_file.save(f'{folder}/{file_name}.{end_prefix}')
        data = {
            'path':f'/static/img/{file_name}.{end_prefix}',
            'url':f'http://127.0.0.1:5000/static/img/{file_name}.{end_prefix}'
        }
        return to_dict_msg(200,data,"上傳圖片成功")
    
def allowed_img(filename):
    return  '.' in filename and filename.rsplit('.' , 1)[1] in Config.ALLOWED_IMGS

def md5_file():
    md5_obj = hashlib.md5()
    md5_obj.update(str(time()).encode())
    file_name = md5_obj.hexdigest()
    return file_name
goods_api.add_resource(Goods,'/goods')