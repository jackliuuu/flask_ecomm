from dotenv import load_dotenv
import os
# 加载 .env 文件
load_dotenv()

class Config:
    MYSQL_DIALECT = os.environ.get('MYSQL_DIALECT')
    MYSQL_DIRVER = os.environ.get('MYSQL_DIRVER')
    MYSQL_NAME = os.environ.get('MYSQL_NAME')
    # MYSQL_PWD = os.environ.get('MYSQL_PWD')
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT'))
    MYSQL_DB = os.environ.get('MYSQL_DB')
    # MYSQL_CHARSET = os.environ.get('MYSQL_CHARSET')
    SQLALCHEMY_DATABASE_URI = f'{MYSQL_DIALECT}+{MYSQL_DIRVER}://{MYSQL_NAME}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    # 默认设置为true，当数据发生变化，会发送一个信号。
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 设置加密字符
    SECRET_KEY = os.urandom(16)
    DEBUG = True

# import pymysql

# def connectdb():
#     print("连接到mysql服务器...")
#     db = pymysql.connect(
#         host="localhost",
#         user="root",
#         passwd="root",
#         port=3306,
#         db="shop_env",
#         charset="utf8",
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     print("连接成功！")
#     return db

# connectdb()

# if __name__=="__main__":
#     print(Config.SQLALCHEMY_DATABASE_URI)
#     connectdb()
