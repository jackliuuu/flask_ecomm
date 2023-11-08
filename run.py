from flask import Flask
from app.product.views import product_bp
from config import Config
from app.product.models import db
from flask_migrate import Migrate
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

# 构建模板文件夹的路径
template_folder = os.path.join(current_dir, 'app', 'templates')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.template_folder = template_folder

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(product_bp)

if __name__ == '__main__':
    app.run()
