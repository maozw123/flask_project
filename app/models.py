from app import models

class BaseModel(models.Model):
    __abstract__ = True #声明当前类是抽象类，被继承调用不被创建
    id = models.Column(models.Integer,primary_key = True,autoincrement=True)
    def save(self):
        db = models.session()
        db.add(self)
        db.commit()
    def delete(self):
        db = models.session()
        db.delete(self)
        db.commit()

#定义表
class Curriculum(BaseModel):
    __tablename__ = "curriculum"
    c_id = models.Column(models.String(32))
    c_name = models.Column(models.String(32))
    c_time = models.Column(models.Date)

class User(BaseModel):
    __tablename__='user'
    user_name=models.Column(models.String(32))
    password=models.Column(models.String(32))
    email=models.Column(models.String(32))

# 请假条
class Leave(BaseModel):
    __tablename__='leave'
    request_id=models.Column(models.Integer)
    request_name=models.Column(models.String(32))
    request_type=models.Column(models.String(32))
    request_start_time=models.Column(models.String(32))
    request_end_time=models.Column(models.String(32))
    request_description=models.Column(models.TEXT)
    request_phone = models.Column(models.String(32))
    request_status=models.Column(models.String(32))

class Picture(BaseModel):
    label=models.Column(models.String(32))
    picture=models.Column(models.String(64))