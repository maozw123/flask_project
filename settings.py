import os

BASE_DIR=os.path.abspath(os.path.dirname(__file__))
STATICFILES_DIR=os.path.join(BASE_DIR,"static")
class Config:
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "ORM.sqlite")  # 数据库地址
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True  #请求结束后自动提交
    SQLALCHEMY_TRACK_MODIFICATIONS=True  #flask1版本之后，添加的选项，目的是跟踪修改
    SECRET_KEY='123123'
class RunConfig(Config):
    DEBUG = False