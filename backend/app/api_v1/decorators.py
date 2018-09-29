# coding=utf-8

'''
这里写一些路由的装饰器，提高部分代码的复用性和简洁性
'''

import functools
from datetime import datetime, timedelta
from flask import jsonify, g, request, session

from app.models.users import user_by_username


def required(*required_args):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
      for arg in required_args:
        if arg not in request.json:
          return jsonify(type='param error', msg='miss some params')
      return func(*args, **kw)
    return wrapper
  return decorator


def login_check(func):
  @functools.wraps(func)
  def wrapper(*args, **kw):
    username = request.json.get('username')
    token = request.headers.get('token')
    if not token or not session.has_key(username):
      return jsonify(type='param error', msg='need to login')
    
    item = session[username]
    if token == item['token']:
      if (datetime.utcnow() - item['timestamp']) <= timedelta(seconds=300):
        return func(*args, **kw)
      # 删除超时的token
      session.pop(username)
      return jsonify(type='param error', msg='login time out')
    return jsonify(type='param error', msg='need to verify your passport')

  return wrapper

          
          