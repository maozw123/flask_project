import os
import json
import hashlib
import datetime
import functools

from flask import jsonify
from flask import session
from flask import request
from flask import redirect
from flask import render_template

# from  main import csrf
from app.models import *
from . import main
from .forms import TaskForm
from app import api
from flask_restful import Resource

class Calendar:
    """
       当前类实现日历功能
       1、返回列表嵌套列表的日历alembic_version
       2、安装日历格式打印日历

       # 如果一号周周一那么第一行1-7号   0
           # 如果一号周周二那么第一行empty*1+1-6号  1
           # 如果一号周周三那么第一行empty*2+1-5号  2
           # 如果一号周周四那么第一行empty*3+1-4号  3
           # 如果一号周周五那么第一行empyt*4+1-3号  4
           # 如果一号周周六那么第一行empty*5+1-2号  5
           # 如果一号周日那么第一行empty*6+1号   6
           # 输入 1月
           # 得到1月1号是周几
           # [] 填充7个元素 索引0对应周一
           # 返回列表
           # day_range 1-30
   """

    def __init__(self, month="now"):
        self.result = []  # 接收所有的日期，需要时一个嵌套列表，列表当中嵌套的是7元素列表
        big_month = [1, 3, 5, 7, 8, 10, 12]
        small_month = [4, 6, 9, 11]
        now = datetime.datetime.now()
        if month == "now":
            month = now.month  # 获取当前月份

            first_date = datetime.datetime(now.year, now.month, 1, 0, 0)  # 获取当月的第一天
        else:
            first_date = datetime.datetime(now.year, month, 1, 0, 0)
        if month in big_month:
            day_range = range(1, 32)
        elif month in small_month:
            day_range = range(1, 31)
        else:
            day_range = range(1, 29)
        self.day_range = list(day_range)  # 获取当前月天数为多少天
        first_week = first_date.weekday()
        line1 = []
        for e in range(first_week):
            line1.append("empty")
            # print(e)
        for d in range(7 - first_week):
            line1.append(str(self.day_range.pop(0)) + '-django开发')
        self.result.append(line1)
        while self.day_range:  # 如果总天数列表有值，就接着循坏:
            line = []
            for i in range(7):
                if len(line) < 7 and self.day_range:
                    line.append(str(self.day_range.pop(0)) + '-django开发')
                else:
                    line.append('empty')
            self.result.append(line)

    def return_month(self):
        """
        返回列表嵌套列表的日历
        """
        return self.result

    def print_month(self):
        print("星期一 星期二  星期三 星期四 星期五 星期六 星期七")
        for line in self.result:
            for day in line:
                day = day.center(6)  # 补全六个字节  中间对齐
                print(day, end='  ')
            print()


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def loginValid(fun):
    @functools.wraps(fun)
    def inner(*args, **kwargs):
        username = request.cookies.get("username")
        id = request.cookies.get("id", "0")
        user = User.query.get(int(id))
        session_username = session.get("username")
        if username and user.user_name == username and username == session_username:
            return fun(*args, **kwargs)
        else:
            return redirect('/login/')

    return inner


@main.route("/logout/")
def logout():
    response = redirect("/login/")
    response.delete_cookie("username")
    response.delete_cookie("email")
    response.delete_cookie("id")
    session.pop('username')
    # del session["username"]
    return response


@main.route('/base/')
def base():
    return render_template('base.html')


@main.route('/login/', methods=['get', 'post'])
def login():
    error = ''
    if request.method == 'POST':
        form_data = request.form
        email = form_data.get('email')
        password = form_data.get('password')
        md5password = setPassword(password)
        user = User.query.filter_by(email=email).first()
        if user:
            db_password = user.password
            if md5password == db_password:
                response = redirect('/index/')
                response.set_cookie('username', user.user_name)
                response.set_cookie('email', user.email)
                response.set_cookie('id', str(user.id))
                session["username"] = user.user_name
                return response
            else:
                error = "密码错误"
        else:
            error = '用户名不存在'
    return render_template('login.html', error=error)


@main.route('/index/')
@loginValid
def index():
    # c=Curriculum()
    # c.c_id="00001"
    # c.c_name='python'
    # c.c_time=datetime.datetime.now()
    # c.save()
    curr_list = Curriculum.query.all()
    return render_template('index.html', curr_list=curr_list)


@main.route('/userinfo/')
def userinfo():
    calender = Calendar(8).return_month()
    now = datetime.datetime.now()
    return render_template('userinfo.html', **locals())


@main.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        new_password = setPassword(password)
        user = User()
        user.user_name = username
        user.password = new_password
        user.email = email
        user.save()
    return render_template('register.html')


@main.route('/holiday_leave/', methods=['GET', 'POST'])
@loginValid
def holiday_leave():
    if request.method == 'POST':
        request_id = request.cookies.get('id')
        request_name = request.form.get("request_user")
        request_type = request.form.get("request_type")
        start_time = request.form.get("start_time")
        request_description = request.form.get("request_description")
        end_time = request.form.get("end_time")
        phone = request.form.get("phone")
        if request_id:
            leave = Leave()
            leave.request_id = request_id
            leave.request_name = request_name
            leave.request_type = request_type
            leave.request_start_time = start_time
            leave.request_end_time = end_time
            leave.request_description = request_description
            leave.request_phone = phone
            leave.request_status = '0'
            leave.save()
            return redirect('/leave_list/1/')
        else:
            return redirect('/login/')
    return render_template('holiday_leave.html')


@main.route('/leave_list/<int:page>/')
def leave_list(page):
    leaves = Leave.query.all()
    pager = Pager(leaves, 2)
    page_data = pager.page_data(page)
    # leaves = Leave.query.offset(0).limit(5)
    return render_template('leave_list.html', **locals())


class Pager:
    """
    flask 分页通过sqlalachemy查询进行分页
    分页器需要具备的功能
    页码
    页码数据
    是否第一页
    是否最后一页
    上一页
    下一页
    """

    def __init__(self, data, page_size):
        """

        :param data: 要分页的数据
        :param page_size: 每页多少条
        """
        self.data = data  # 总数据
        self.page_size = page_size  # 单页数据
        self.is_start = False
        self.is_end = False
        self.page_count = len(data)
        self.next_page = 0  # 上一页
        self.previous_page = 0  # 下一页
        self.page_number = self.page_count / page_size
        if self.page_number == int(self.page_number):
            self.page_number = int(self.page_number)
        else:
            self.page_number = int(self.page_number) + 1
        self.page_range = range(1, self.page_number)  # 页码范围

    def page_data(self, page):
        """
        返回分页数据
        :param page: 页码
        page_size=10
        1  start 0  end  10
        2  start 10  end  20
        3  start 20  end  30
        """
        self.next_page = int(page) + 1
        self.previous_page = int(page) - 1
        if page <= self.page_range[-1]:
            page_start = (page - 1) * self.page_size
            page_end = page * self.page_size
            data = self.data[page_start:page_end]
            if page == 1:
                self.is_start = True
            else:
                self.is_start = False
            if page == self.page_range[-1]:
                self.is_end = True
            else:
                self.is_end = False
        else:
            data = ['没有数据']
        return data



@main.route('/add_task/', methods=["GET", "POST"])
def add_task():
    """
        print(task.errors) 表单校验错误
        print(task.validate_on_submit()) 判断是否是一个有效的post请求
        print(task.validate()) 判断是否是一个合法的post请求
        print(task.data) 提交的数据
        """
    task = TaskForm()
    return render_template("add_task.html", **locals())





@main.route('/cancel/', methods=['GET', 'POST'])
def cancel():
    # data1=request.args
    # data2=request.data
    # data3=request.form
    id = request.form.get("id")  # 通过args接受get请求数据
    leave = Leave.query.get(int(id))
    leave.delete()
    return jsonify({"data": "删除成功"})  # 返回json数据


from settings import STATICFILES_DIR


@main.route('/picture/', methods=["GET", "POST"])
def picture():
    p = {"picture": "img/1.jpg"}
    if request.method == "POST":
        file = request.files.get('photo')
        file_name = file.filename
        file_path = 'img/%s' % file_name
        save_path = os.path.join(STATICFILES_DIR, file_path)
        file.save(save_path)
        p = Picture()
        p.picture = file_path
        p.save()
    return render_template('picture.html', p=p)


@api.resource("/Api/leave/")
class LeaveApi(Resource):
    def __init__(self):
        super(LeaveApi,self).__init__()
        self.result={
            "version":"1.0",
            "data":""
        }
    def set_data(self,leave):
        result_data={
            "request_name":leave.request_name,
            "request_type":leave.request_type,
            "request_start_time":leave.request_start_time,
            "request_end_time":leave.request_end_time,
            "request_description":leave.request_name,
            "request_phone":leave.request_phone,
        }
        return result_data
    def get(self):
        data=request.args
        id=data.get("id")
        if id:
            leave=Leave.query.get(int(id))
            result_data=self.set_data(leave)
        else:
            leaves=Leave.query.all()
            result_data=[]
            for leave in leaves:
                result_data.append(self.set_data(leave))
        self.result["data"]=result_data
        return self.result
    def post(self):
        data=request.form
        request_id = data.get("request_id")
        request_name = data.get("request_name")
        request_type = data.get("request_type")
        request_start_time = data.get("request_start_time")
        request_end_time = data.get("request_end_time")
        request_description = data.get("request_description")
        request_phone = data.get("request_phone")

        leave=Leave()
        leave.request_id = request_id
        leave.request_name = request_name
        leave.request_type = request_type
        leave.request_start_time = request_start_time
        leave.request_end_time = request_end_time
        leave.request_description = request_description
        leave.request_phone = request_phone
        leave.request_status = '0'
        leave.save()

        self.result["data"]=self.set_data(leave)
        return self.result
    def put(self):
        data=request.form
        id=data.get("id")
        leave=Leave.query.get(int(id))
        for key,value in data.items():
            if key !="id":
                setattr(leave,key,value)
        leave.save()
        self.result["data"] = self.set_data(leave)
        return self.result
    def delete(self):
        data=request.form
        id=data.get("id")
        leave=Leave.query.get(int(id))
        leave.delete()
        self.result["data"] = "%s 删除成功" % id
        return self.result
