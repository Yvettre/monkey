# coding=utf-8

from datetime import datetime
from flask import current_app

from app import db
from config import config


class User(db.Model):
  '''
  用户对象
  '''
  # 表名，遵守复数形式的命名约定
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255), unique=True, index=True)
  email = db.Column(db.String(255), unique=True, index=True)
  passwd_hash = db.Column(db.String(128))
  register_time = db.Column(db.DateTime, default=datetime.utcnow)
  last_login = db.Column(db.DateTime, default=datetime.utcnow)

  @property
  def passwd(self):
    '''
    设定passwd属性为不可读
    '''
    raise AttributeError('passwd is not a readable attribute')


  def _add_salt_encrypt(self, passwd):
    '''
    使用hashlib.sha256加盐加密，返回加密后字符串
    64位的16进制字符串
    '''
    import hashlib
    salt = current_app.config['SALT']
    return hashlib.sha256(salt + passwd + self.username).hexdigest()


  @passwd.setter
  def passwd(self, passwd):
    self.passwd_hash = self._add_salt_encrypt(passwd)


  def verify_passwd(self, passwd):
    '''
    密码验证
    '''
    return self.passwd_hash == self._add_salt_encrypt(passwd)

  
  def update_last_login(self):
    '''
    更新最近一次的登入时间
    '''
    self.last_login = datetime.utcnow()
 

  def generate_token(self):
    '''
    根据用户信息生成加密token，用于记录用户会话
    '''
    import hashlib
    key = current_app.config['SECRET_KEY']
    return hashlib.sha224(key + self.email + str(self.last_login)).hexdigest()


  def get_info_json(self):
    '''
    返回用户信息，以json的格式
    '''
    return {
      'user_id': self.id,
      'username': self.username,
      'email': self.email
    }

  
  def __repr__(self):
    '''
    返回一个可读性的字符串表示模型，可用于调试
    注意不是%s
    '''
    return '<User %r>' % self.username
  
  # todo:用户头像、管理员角色


def create_user(username, email, passwd):
  '''
  根据信息创建用户，并将用户记录加入到数据库中
  如果成功返回用户的主键id
  如果出错将回滚并返回0
  '''
  user = User()
  user.email = email
  user.username = username
  user.passwd = passwd      # 利用了User类中的passwd属性的方法间接加密了用户密码

  try:
    db.session.add(user)
    db.session.commit()
  except Exception as e:
    current_app.logger.error(e)
    db.session.rollback()
    return 0
  
  return user.id


def delete_user(user):
  '''
  根据用户对象删除用户在数据库中的相关记录
  '''
  try:
    db.session.delete(user)
    db.session.commit()
  except Exception as e:
    current_app.logger.error(e)
    db.session.rollback()
    return False  
  return True


def user_by_username(username):
  '''
  根据username返回数据库中的用户对象
  '''
  user = User.query.filter_by(username=username).first()
  if user is not None:
    return user
  return None


def user_by_email(email):
  '''
  根据email返回数据库中的用户对象
  '''
  user = User.query.filter_by(email=email).first()
  if user is not None:
    return user
  return None

