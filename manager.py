# manager.py
# 只负责运行项目

# 引入db
from app import create_app,db
# MigrateCommand migrate的命令
from flask_migrate import Migrate
# 管理:方便数据库的同步
from flask_script import Manager

app = create_app('develop')
app.config['SECRET_KEY'] = 'jack_test'

# migrate和同步数据库配置
manager = Manager(app)
Migrate(app,db)

if __name__ == "__main__":
    manager.run()
