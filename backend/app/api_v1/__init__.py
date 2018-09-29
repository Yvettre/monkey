# coding=utf-8

from flask import Blueprint


'''
通过实例化一个Blueprint类对象来创建蓝图
构造函数中必须两个参数：蓝图的名字、蓝图所在的包或模块（一般用__name__变量即可）
'''
api = Blueprint('api', __name__)


'''
由于在passport等包中还需要导入蓝图api
为了避免循环导入，必须加上这句
'''
from . import passport