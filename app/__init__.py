from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_restful import Api

import pymysql
pymysql.install_as_MySQLdb()

csrf=CSRFProtect()
models=SQLAlchemy()
api=Api()

def create():
    app=Flask(__name__)
    app.config.from_object("settings.Config")  #来源于类对象
    models.init_app(app)
    # csrf.init_app(app)
    api.init_app(app)
    from .mian import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app