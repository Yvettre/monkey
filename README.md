## 前后端分离：Flask实现后台RESTful web API

不使用Flask-restful包，实现一个具有RESTful特性的web后台接口

### 一、工程目录结构
```
- monkey
|--- backend
|      |--- log
|      |--- migrations
|      |--- tests
|      |--- venv
|      |--- app
|      |     |--- api_v1
|      |     |--- models
|      |     |--- __init__.py
|      |--- config.py
|      |--- manage.py
|      |--- utils.py
|--- frontend
|--- README.md
```

### 二、后台实现

#### 1. 目前功能
- 实现了用户注册、登录、登出、获取用户信息、删除账户五个接口
- 登录后使用token保持会话，token有效期是5分钟，过期需重新登录
- 获取用户信息需要用户登录
- 删除账户需要密码验证

#### 2. Todo
- 增加用户角色分类（管理员、普通用户等）
- 注册邮箱验证码
- cookie
- 丰富用户信息（如个性签名、头像等）
- 注册信息字符要求以及支持中文用户名
- 增加可修改用户部分信息功能（如密码等）
- 增加单元测试功能
- 。。。


### 三、前端实现

#### 1. Todo
Vue + Vue-router + axios



### 四、Usage

#### 1. 环境（Environments）
- python-2.7.14
- MySQL-5.7.23

#### 2. 运行后台

- 打开根目录：``cd backend``
- 创建虚拟环境并激活（Linux下没有.bat后缀）
  ```
  vitualenv -p C:\python27\python.exe --no-site-packages venv
  venv\Script\activate.bat
  ```
- 安装python相关packages：``pip install -r requirements.txt``
- 初始化并生成数据库表
  ```
  python manager.py db init
  python manager.py db migrate -m "initial migrate"
  python manager.py db upgrade
  ```
- 运行后台服务：``python manage.py runserver``

#### 3. 运行前端（或打包配置nginx等）
todo