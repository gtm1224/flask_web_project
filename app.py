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

class user(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    realname = db.Column(db.String)
    sex = db.Column(db.Integer)
    mylike = db.Column(db.String)
    city = db.Column(db.String)
    intro = db.Column(db.String)

@app.route("/register")
def register():
    return render_template("register.html")

@app.context_processor
def account():
    return {"username":username}