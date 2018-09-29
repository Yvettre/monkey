# coding=utf-8

import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import config
from utils import setup_logger

db = SQLAlchemy()


def create_app(app_env):
  '''
  根据配置名称显式调用工厂函数，创建创建app实例
  原因：如果程序在全局作用域中创建，配置就无法动态修改，不利于单元测试
  '''
  # 创建日志
  logger = setup_logger(config[app_env].LOGGER_NAME, 
                        config[app_env].LOGGING_LEVEL)

  app = Flask(__name__)
  # 使用app.config对象提供的from_object()函数直接导入对应配置
  app.config.from_object(config[app_env])
  # 允许跨域请求资源
  CORS(app, supports_credentials=True)

  # 初始化db实例
  db.init_app(app)

  # 注册api_v1蓝图
  from app.api_v1 import api as api_v1_0_blueprint
  app.register_blueprint(api_v1_0_blueprint, url_prefix='/api/v1.0')

  return app