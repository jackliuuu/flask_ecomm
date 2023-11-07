from flask import Blueprint
# 创建蓝图，记得要注册
#定义好传递给的变量 蓝图对象名称      前缀名                  
user = Blueprint('user', __name__, url_prefix='/user')

from user import view
