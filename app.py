from flask import Flask, render_template, request
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
@app.route("/userlist",methods=['get'])
def userList():
    users = User.query.all()
    return render_template("user/user_list.html",users=users)