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
    # 获取到字典中的哪种类，获取到对应的类名，再给到from_object获取到对应的参数
    obj = config_map.get(config_name)
    # 加载数据库到Flask中
    app.config.from_object(obj)
    # 默认连接数据库
    db.init_app(app)
    
    # 注册用户的蓝图
    # 不可以把这一行放到开头，否则会执行回init，再引用回来会需要创建db，产生报错
    from app.user import user
    
    app.register_blueprint(user)

    return app

