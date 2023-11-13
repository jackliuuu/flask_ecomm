from dotenv import load_dotenv
import os
# 加载 .env 文件
load_dotenv()

class Config:
    ALLOWED_IMGS = set(['bmp','png','jpg','jpeg','gif'])
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVER_IMG_UPLOADS = os.path.join(BASE_DIR,'app','static','img') 

    MYSQL_DIALECT = os.environ.get('MYSQL_DIALECT')
    MYSQL_DIRVER = os.environ.get('MYSQL_DIRVER')
    MYSQL_NAME = os.environ.get('MYSQL_NAME')
    # MYSQL_PWD = os.environ.get('MYSQL_PWD')
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT'))
    MYSQL_DB = os.environ.get('MYSQL_DB')
    # MYSQL_CHARSET = os.environ.get('MYSQL_CHARSET')
    SQLALCHEMY_DATABASE_URI = f'{MYSQL_DIALECT}+{MYSQL_DIRVER}://{MYSQL_NAME}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4'
    # 默认设置为true，当数据发生变化，会发送一个信号。
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 设置加密字符
    SECRET_KEY = os.urandom(16)
    DEBUG = True


