# coding:utf-8

import os
from flask import Flask


def create_app(test_config=None):
    # create and config the app
    # 创建Flask实例
    # __name__是当前python模块的名称，应用需要知道在那里设置路径，使用__name__很方便
    # instance_relative_config=True告诉应用配置文件是相对于instance folder的相对路径。实例文件夹在flaskr包外面
    # 用于存放本地数据，不应该提交到版本控制系统
    # 实例文件夹：
    app = Flask(__name__, instance_relative_config=True)
#    app.config.from_mapping()设置一个应用的默认配置
    # SECRET_KEY是被flask和扩展用于数据安全的。在开发过程中，为了方便设置为dev,但在发布时应使用随机值重载它
    # DATABASE SQLite数据库文件存放路径，位于FLASK用于存放实例的app.instance_path之内，后面细说
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if test_config is None:
        # load the instance config,if it exists,when not testing)
        # 如果有config.py,使用config.py中的值来重载默认值，正式部署时候可以用来设置一个真正的SECRET_KEY
        # test_config也会被传递给工厂，并且会代替实例配置，这样可以实现测试嗯哼开发的配置分离，相互独立。
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        #
        app.config.from_mapping(test_config)

    # ensure the instance folder existe
    try:
        # 确保app.instance_path存在，flask不会自动给创建实例文件夹，但是必须确保创建这个文件夹
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return "hello world!"


    # 居然不能用from py-api import db
    # 这个就算是注册了吗？

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
