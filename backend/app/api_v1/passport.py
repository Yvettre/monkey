# coding=utf-8

'''
用于写用户注册、登录和登出的业务逻辑
'''

from flask import g, current_app, request, make_response, jsonify, session
from flask import redirect, url_for

from app import db
from app.api_v1 import api

from app.models.users import create_user, user_by_username, user_by_email
from app.models.users import delete_user

from decorators import required, login_check



@api.route('/register', methods=['POST'])
@required('username', 'email', 'passwd')
def register():
  '''
  用户注册接口
  todo: 用户名支持中文，用户名和密码加正则匹配检验
  '''
  username = request.json.get('username')
  email = request.json.get('email')

  # 判断当前用户填写的注册邮箱和用户名是否已被注册
  if user_by_username(username) is not None:
    return jsonify(type='param error', msg='username is been used.')
  if user_by_email(email) is not None:
    return jsonify(type='param error', msg='email is been used.')
  
  # 创建新用户并写入数据库
  uid = create_user(username, email, request.json.get('passwd'))
  if uid == 0:
    return jsonify(type='db error', msg='register fail')
  return jsonify(type='OK', msg='register seccess')



@api.route('/login', methods=['POST'])
@required('username', 'passwd')
def login():
  '''
  登录接口
  '''
  username = request.json.get('username')
  
  user = user_by_username(username)
  if user is None:
    return jsonify(type='param error', msg='username is not registered.')
  
  # 验证登录密码
  if user.verify_passwd(request.json.get('passwd')):
    # 验证成功
    # 更新登入时间
    user.update_last_login()
    # 生成加密token
    token = user.generate_token()
    timestamp = user.last_login
    # 将用户的token信息加入会话
    session[username] = {'token':token, 'timestamp':timestamp}
    # 返回登录成功信息
    return jsonify(type='OK', msg='login OK', token=session[username]['token'])

  return jsonify(type='param error', msg='username or passwd error.')


@api.route('/logout', methods=['POST'])
@login_check
def logout():
  '''
  登出接口
  '''
  username = request.json.get('username')
  # 从session中删除相关用户的token
  session.pop(username)
  return jsonify(type='OK', msg='logout OK')


@api.route('/user/<path:username>', methods=['POST'])
@login_check
def user(username):
  '''
  用户主页基本信息接口
  '''
  user = user_by_username(username) 
  return jsonify(user.get_info_json())
  

@api.route('/delete/<path:username>', methods=['POST'])
@required('passwd')
@login_check
def delete_account(username):
  '''
  注销用户，从数据库中删除用户的相关记录
  '''
  user = user_by_username(username)

  # 验证密码
  if user.verify_passwd(request.json.get('passwd')):
    if delete_user(user):
      session.pop(username)
      return jsonify(type='OK', msg='delete user OK')
    return jsonify(type='db error', msg='delete user fail')
  return jsonify(type='param error', msg='delete user fail')

