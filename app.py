from flask import Flask, render_template, request,redirect,url_for
from libs import db
from views.users import user_app
from views.articles import article_app
from flask_migrate import Migrate
from models import Category
# init db
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my.db"
db.init_app(app)
# 添加user和articleblueprint
app.register_blueprint(user_app,url_prefix="/user")
app.register_blueprint(article_app,url_prefix="/article")

@app.route("/")
def index():

    return render_template("index.html")

# using get method to test form
# @app.route('/login', methods=['get','post'])
# def login():
#     username = request.args.get("username")
#     password = request.args.get("password")
#     print(username, password)
#     return render_template("login.html")

# simplify the submitted address:
# @app.route('/login/<username>/<password>/')
# def login(username,password):
#     # username = request.args.get("username")
#     # password = request.args.get("password")
#     print(username,password)
#     return render_template("login.html")

# using post method:
@app.route('/login',methods= ['get','post'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("<---------------------------->")
        print(username,password)
    return render_template("login.html")


@app.context_processor
def account():
    cates = Category.query.all()
    return {"cates":cates}



migrate = Migrate(app,db,render_as_batch=True)

# class User(db.Model):
#     id = db.Column(db.Integer,primary_key = True)
#     username = db.Column(db.String)
#     password = db.Column(db.String)
#     realname = db.Column(db.String)
#     sex = db.Column(db.Integer)
#     mylike = db.Column(db.String)
#     city = db.Column(db.String)
#     intro = db.Column(db.String)

# @app.route("/register",methods=['get','post'])
# def register():
#     if request.method == "POST":
#         realname = request.form['name']
#         username = request.form['username']
#         password = request.form['password']
#         sex = request.form['sex']
#         mylike ='|'.join(request.form.getlist('like'))
#         city = request.form['city']
#         intro = request.form['intro']
#         user = User(
#             realname=realname,
#             username = username,
#             password =password,
#             sex = sex,
#             mylike = mylike,
#             city = city,
#             intro = intro
#         )
#         db.session.add(user)
#         db.session.commit()
#     return render_template("register.html")

# @app.context_processor
# def account():
#     return {"username":username}


# def createBatchUsers():
#     words = list("abcdefghijklmnopqrstuvwxyz")
#     citys = ["010","021","0512"]
#     mylikes = ["睡觉","旅游","看书","唱歌"]
#     import random
#     for i in range(100):
#         random.shuffle(words)
#         username="".join(words[:6])
#         sex = random.randint(0,1)
#         city = citys[random.randint(0,2)]
#         random.shuffle(mylikes)
#         mylike = "|".join(mylikes[:random.randint(0,3)])
#         user = User(
#             realname="-",
#             username=username,
#             password="",
#             sex=sex,
#             mylike=mylike,
#             city=city,
#             intro=""
#         )
#         db.session.add(user)
#     db.session.commit()

# get user list
# @app.route("/userlist",methods=['get','post'])
# def userList():
#     if request.method == "POST":
#         q = request.form['q']
#         # print(q)
#         # condition = {request.form['field']:q}
#         # print(condition)
#         field = request.form['field']
#         if field == "realname":
#             condition = User.realname.like('%%%s%%' % q)
#             # print("<<<<<<>>>>>>>>")
#             # print(('%%%s%%' % q))
#         else:
#             # use filter like
#             condition = User.username.like('%%%s%%' % q)
#             # use filter_by
#             #users = User.query.filter_by(**condition).all()
#         order_type = request.form['order']
#         if order_type == "1":
#             order = User.id.asc()
#         else:
#             order = User.id.desc()
#         users = User.query.filter(condition,User.sex==request.form['sex']).order_by(order).paginate(1,5)
#         query_string =""
#     else:
#         # return redirect(url_for(userList2))
#         # users = User.query.all()
#         # add pages
#         page = request.args.get('page',1)
#         # print('wwwwwww',page)
#         # 如果提交了查询关键词q
#         q = request.args.get('q')
#         print("qqqqqqqqqqqqqqqqqqqqqqq",q)
#         if q:
#             print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
#             field = request.args.get('field')
#             print(field)
#             if field == "realname":
#                 condition = User.realname.like('%%%s%%' % q)
#             else:
#                 condition = User.username.like('%%%s%%' % q)
#
#             order_type = request.args.get('order')
#             if order_type == "1":
#                 order = User.id.asc()
#             else:
#                 order = User.id.desc()
#
#             sex = request.args.get('sex', 1)
#             users = User.query.filter(condition, User.sex == sex).order_by(order).paginate()
#             # 拼接查询条件（相当于request的query_string属性）
#             # 在模版的翻页部分添加上query_string
#             query_string = "q=" + q + "&field=" + field + "&sex=" + sex + "&order=" + order_type + "&page="+ page
#             print("sssssssss",query_string)
#         else:
#             users = User.query.paginate(int(page), 10)
#             query_string = ""
#         print(query_string)
#     return render_template("user/user_list.html", users=users.items,
#                                pages=users.pages,
#                                total=users.total,
#                                pageList=users.iter_pages(),
#                                condition=query_string
#                                )


# # delete user by id:
# @app.route("/user_delete/<int:user_id>")
# def deleteUser(user_id):
#     user = User.query.get(user_id)
#     db.session.delete(user)
#     db.session.commit()
#     return redirect(url_for("userList"))
#
# # edit user info:
# @app.route("/useredit/<int:user_id>",methods=['get','post'])
# def editUser(user_id):
#     user = User.query.get(user_id)
#     if request.method == "POST":
#         user.username = request.form['username']
#         user.realname = request.form['name']
#         user.sex = request.form['sex']
#         user.mylike = "|".join(request.form.getlist('like'))
#         user.city = request.form['city']
#         user.intro = request.form['intro']
#         db.session.commit()
#         return redirect(url_for("userList"))
#     return render_template("user/edit_user.html",user=user)