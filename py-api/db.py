import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # g是一个特殊对象，独立于每一个请求，再请求过程中，它可以用来存储多个函数用到的数据，把连接存储再其中，可以多次使用，
    # 而不用再同一个请求中每次调用get_db时都创建一个新的连接
    if 'db' not in g:
        g.db = sqlite3.connect(
            # Current_app是另一个特殊对象指向当前正在处理请求的flask应用，因为用了应用工厂（不明白），
            # 所以再后续的编程中没有应用对象，get_bd将在应用创建时且正在处理请求时调用，因此current_app可以用
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """clear the existing data and create new tables."""
    init_db()
    click.echo('initialized the database.')


def init_app(app):
    # 告诉flask在返回相应后进行清理的时候调用此函数
    app.teardown_appcontext(close_db)
    # 添加一个新的可以与flask一起工作的命令。
    app.cli.add_command(init_db_command)