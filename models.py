from libs import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    realname = db.Column(db.String)
    sex = db.Column(db.Integer)
    mylike = db.Column(db.String)
    city  = db.Column(db.String)
    intro = db.Column(db.String)

    def hash_password(self,password):
        self.password = generate_password_hash(password)

    def validate_password(self,password):
        return check_password_hash(self.password,password)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    intro = db.Column(db.String)
    content = db.Column(db.Text)
    author = db.Column(db.String)
    pubdate = db.Column(db.DateTime, default=datetime.utcnow)
    cate_id = db.Column(db.Integer,db.ForeignKey("category.cate_id"))

class Category(db.Model):
    cate_id = db.Column(db.Integer,primary_key=True)
    cate_name = db.Column(db.String,unique = True)
    cate_order = db.Column(db.Integer,default=0)
    articles = db.relationship("Article",cascade="delete")
