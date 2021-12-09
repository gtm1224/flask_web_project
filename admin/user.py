from flask import request,session,render_template,\
                  redirect, url_for

from .admin_app import admin_app
from models import User
from libs import db
import json


# 验证用户名是否重复
def validate_username(username):
    return User.query.filter_by(username=username).first()

# 获得用户列表
# 如果用户刚进入列表页是访问http://127.0.0.1/user/list
# 与"/list/<int:page>"不匹配，提供一个默认带有page默认值
# 的路由
@admin_app.route("/user/list/<int:page>",methods=['get',"post"])
@admin_app.route("/user/list",defaults={"page":1},methods=['get',"post"])
def userList(page):
    if request.method == "POST":
        q = request.form['q']
        # print(q)
        # condition = {request.form['field']:q}
        # print(condition)
        field = request.form['field']
        if field == "realname":
            condition = User.realname.like('%%%s%%' % q)
            # print("<<<<<<>>>>>>>>")
            # print(('%%%s%%' % q))
        else:
            # use filter like
            condition = User.username.like('%%%s%%' % q)
            # use filter_by
            #users = User.query.filter_by(**condition).all()
        order_type = request.form['order']
        if order_type == "1":
            order = User.id.asc()
        else:
            order = User.id.desc()
        users = User.query.filter(condition,User.sex==request.form['sex']).order_by(order).paginate(page,5)
        query_string =""
    else:
        # return redirect(url_for(userList2))
        # users = User.query.all()
        # add pages
        page = request.args.get('page',1)
        # print('wwwwwww',page)
        # 如果提交了查询关键词q
        q = request.args.get('q')
        print("qqqqqqqqqqqqqqqqqqqqqqq",q)
        if q:
            print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
            field = request.args.get('field')
            print(field)
            if field == "realname":
                condition = User.realname.like('%%%s%%' % q)
            else:
                condition = User.username.like('%%%s%%' % q)

            order_type = request.args.get('order')
            if order_type == "1":
                order = User.id.asc()
            else:
                order = User.id.desc()

            sex = request.args.get('sex', 1)
            users = User.query.filter(condition, User.sex == sex).order_by(order).paginate()
            # 拼接查询条件（相当于request的query_string属性）
            # 在模版的翻页部分添加上query_string
            query_string = "q=" + q + "&field=" + field + "&sex=" + sex + "&order=" + order_type + "&page="+ page
            print("sssssssss",query_string)
        else:
            users = User.query.paginate(int(page), 10)
            query_string = ""
        print(query_string)
    return render_template("admin/user/user_list.html", users=users.items,
                               pages=users.pages,
                               total=users.total,
                               pageList=users.iter_pages(),
                               condition=query_string
                               )

# 根据用户id删除用户
@admin_app.route("/delete/<int:user_id>")
def deleteUser(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for(".userList"))

# 用户信息修改
@admin_app.route("/user/edit/<int:user_id>", methods=['get', 'post'])
def editUser(user_id):
    user = User.query.get(user_id)
    if request.method == "POST":
        user.username = request.form['username']
        user.realname = request.form['name']
        user.sex = request.form['sex']
        user.mylike = "|".join(request.form.getlist('like'))
        user.city = request.form['city']
        user.intro = request.form['intro']
        db.session.commit()
        return redirect(url_for(".userList"))
    return render_template("admin/user/user_edit.html", user=user)
