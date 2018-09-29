# coding=utf-8

import logging
import os


class BaseConfig(object):
  # 防止CSRF攻击的用于生成token的字符串
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SALT = os.environ.get('SALT')

  # logger name
  LOGGER_NAME = 'monkey'

  # SQLALchemy配置
  SQLALCHEMY_COMMIT_ON_TEARDOWN = True   # 每次请求结束后都会自动提交数据库的变动
  SQLALCHEMY_TRACK_MODIFICATIONS = True  # 开启跟踪


class DevelopConfig(BaseConfig):
  '''
  开发环境配置
  '''
  DEBUG = True
  LOGGING_LEVEL = logging.DEBUG

  # 开发环境用的数据库连接
  # 生产环境应从环境中获取用户名和密码等敏感信息
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@127.0.0.1:3306/monkey'.format(
    os.environ.get('MYSQL_USER'), os.environ.get('MYSQL_PASSWD'))


class TestConfig(BaseConfig):
  '''
  测试环境配置/单元测试与持续集成
  '''
  TESTING = True
  LOGGING_LEVEL = logging.WARNING

  # 测试环境用的数据库连接
  # SQLALCHEMY_DATABASE_URI = ''


class ProductionConfig(BaseConfig):
  '''
  生产环境配置
  '''
  DEBUG = False

  # 生产环境用的数据库连接
  # SQLALCHEMY_DATABASE_URI = ''


config = {
  'development': DevelopConfig,
  'testing': TestConfig,
  'production': ProductionConfig,

  'default': DevelopConfig
}