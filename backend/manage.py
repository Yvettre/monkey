# coding=utf-8

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand   # 便于数据库模型的修改、更新等

from app import create_app, db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migarate = Migrate(app, db)


'''
向命令行解释器manager中添加命令
'''
manager.add_command('db', MigrateCommand)


'''
数据库迁移操作指令（类似git的一种数据库版本控制）
创建迁移仓库（./migrations）：python manager.py db init
自动创建迁移脚本：python manager.py db migrate -m "initial migrate"
更新数据库：python manager.py db upgrade
'''


if __name__ == '__main__':
  manager.run()