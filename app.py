from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my.db"

db=SQLAlchemy(app)

@app.route("/")
def index():
    lists = [
        {"title":"头条新闻","intro":"BTC reaches all time high!"},
        {"title": "头条新闻", "intro": "BTC reaches all time high!"},
        {"title": "头条新闻", "intro": "BTC reaches all time high!"},
    ]
    return render_template("index.html",newsLists = lists)

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
username = None
# using post method:
@app.route('/login',methods= ['get','post'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("<---------------------------->")
        print(username,password)
    return render_template("login.html")

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    realname = db.Column(db.String)
    sex = db.Column(db.Integer)
    mylike = db.Column(db.String)
    city = db.Column(db.String)
    intro = db.Column(db.String)

@app.route("/register",methods=['get','post'])
def register():
    if request.method == "POST":
        realname = request.form['name']
        username = request.form['username']
        password = request.form['password']
        sex = request.form['sex']
        mylike ='|'.join(request.form.getlist('like'))
        city = request.form['city']
        intro = request.form['intro']
        user = User(
            realname=realname,
            username = username,
            password =password,
            sex = sex,
            mylike = mylike,
            city = city,
            intro = intro
        )
        db.session.add(user)
        db.session.commit()
    return render_template("register.html")

@app.context_processor
def account():
    return {"username":username}


def createBatchUsers():
    words = list("abcdefghijklmnopqrstuvwxyz")
    citys = ["010","021","0512"]
    mylikes = ["睡觉","旅游","看书","唱歌"]
    import random
    for i in range(100):
        random.shuffle(words)
        username="".join(words[:6])
        sex = random.randint(0,1)
        city = citys[random.randint(0,2)]
        random.shuffle(mylikes)
        mylike = "|".join(mylikes[:random.randint(0,3)])
        user = User(
            realname="-",
            username=username,
            password="",
            sex=sex,
            mylike=mylike,
            city=city,
            intro=""
        )
        db.session.add(user)
    db.session.commit()

# get user list
@app.route("/userlist",methods=['get','post'])
def userList():
    if request.method == "POST":
        q = request.form['q']
        # print(q)
        # condition = {request.form['field']:q}
        # print(condition)
        if request.form['field'] == "realname":
            condition = User.realname.like('%%%s%%' % q)
            print("<<<<<<>>>>>>>>")
            print(('%%%s%%' % q))
        else:
            condition = User.username.like('%%%s%%' % q)
    # use filter_by
    #     users = User.query.filter_by(**condition).all()
    # use filter like
        users = User.query.filter(condition).all()

    else:
        users = User.query.all()
    return render_template("user/user_list.html",users=users)

# delete user by id:
@app.route("/user_delete/<int:user_id>")
def deleteUser(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("userList"))

# edit user info:
@app.route("/useredit/<int:user_id>",methods=['get','post'])
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
        return redirect(url_for("userList"))
    return render_template("user/edit_user.html",user=user)