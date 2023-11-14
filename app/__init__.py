from flask import Flask
# 导入数据库
from flask_sqlalchemy import SQLAlchemy
# 获取是哪种开发模式
from config import Config
# 先不连接app对象，否则报错，在下面创建app对象时默认连接数据库，就可以了
db = SQLAlchemy()


class DevelopmentConfig(Config):
    DEBUG = True
# 生产模式，关闭debug模式
class ProductionConfig(Config):
    pass


config_map={
    'develop':DevelopmentConfig,
    'product':ProductionConfig
}


def create_app(config_name):
    app = Flask(__name__)
    # 
    obj = config_map.get(config_name)
    # 把DB資訊丟進去flask
    app.config.from_object(obj)
    app.config['SQLALCHEMY_DATABASE_URI']=Config.SQLALCHEMY_DATABASE_URI
    app.config['JSON_AS_ASCII'] = False
    #初始化DB
    db.init_app(app)
    
    #註冊blueprint
    #不能讓from 被init
    from app.user import user
    app.register_blueprint(user)
    
    from app.menu import menu
    app.register_blueprint(menu)
    
    from app.role import role
    app.register_blueprint(role)
    
    from app.category import category
    app.register_blueprint(category) 
    
    from app.category import attribute
    app.register_blueprint(attribute)
    
    from app.goods import goods
    app.register_blueprint(goods)
    
    from app.order import order
    app.register_blueprint(order)
    
    return app

