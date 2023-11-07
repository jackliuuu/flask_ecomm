# manager.py
# 只负责运行项目

# 引入db
from init import create_app,db
# MigrateCommand migrate的命令
from flask_migrate import Migrate,MigrateCommand
# 管理:方便数据库的同步
from flask_script import Manager

app = create_app('develop')

# migrate和同步数据库配置
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)

if __name__ == "__main__":
    # app.run()
    # flask专门管理的命令
    manager.run()
