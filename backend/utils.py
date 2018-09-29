# coding=utf-8

import os
import datetime
import logging
import logging.handlers

from flask import Response

def setup_logger(name, level):
  '''
  创建日志
  '''
  # logger settings
  time_format = '%Y-%m-%d-%H-%M-%S'
  time_now = datetime.datetime.now()
  log_file = 'log/log_%s.log' %time_now.strftime(time_format)
  log_file_max_size = 1024 * 1024 * 20 # megabytes
  log_num_backups = 3
  log_format = '%(asctime)s [%(levelname)s]: %(filename)s(%(funcName)s:%(lineno)s) >> %(message)s'
  log_date_format = '%m/%d/%Y %I:%M:%S %p'
  log_filemode = 'w'  # w:overwrite   a:append

  # setup logger
  # datefmt=log_date_format
  logging.basicConfig(filename=log_file, format=log_format, filemode=log_filemode, level=level)
  rotate_file = logging.handlers.RotatingFileHandler(
      log_file, maxBytes=log_file_max_size, backupCount=log_num_backups
  )
  logger = logging.getLogger(name)
  logger.addHandler(rotate_file)

  # print log messages to console
  consoleHandler = logging.StreamHandler()
  logFormatter = logging.Formatter(log_format)
  consoleHandler.setFormatter(logFormatter)
  logger.addHandler(consoleHandler)

  return logger


def json_response(str, re_code):
  '''
  根据str构造http响应并返回
  '''
  resp = Response(response=str, status=re_code, mimetype='application/json')
  return resp