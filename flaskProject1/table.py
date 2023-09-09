from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from flask_cors import *
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)

## 数据库配置信息
HOSTNAME = "rm-2zenmvh0jxuzf9wtk4o.mysql.rds.aliyuncs.com"
PORT = "3306"
USERNAME = "blog"
PASSWORD = "HUpy2333!"
DATABASE = "sf"
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
db = SQLAlchemy(app)


## 表
@dataclass
class User(db.Model):
    __tablename__ = "user"  ##表名

    uid: str
    secret: str
    sign: str
    uname: str
    avatar: str

    uid = db.Column(db.String(20), primary_key=True)
    secret = db.Column(db.String(20), nullable=False)
    sign = db.Column(db.String(20))
    uname = db.Column(db.String(20), nullable=False)
    avatar = db.Column(db.String(100))


@dataclass
class Img(db.Model):
    __tablename__ = 'img'

    iid: int
    uid: str
    source: str
    tag: str
    title: str
    prompt: str
    n_prompt: str
    time: str

    iid = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    tag = db.Column(db.String(4), nullable=False)
    prompt = db.Column(db.String(150))
    n_prompt = db.Column(db.String(100))
    time = db.Column(db.DateTime,nullable=False,default = datetime.now)

    uid = db.Column(db.String(20),db.ForeignKey("user.uid"),nullable=False)


@dataclass
class Like(db.Model):
    __tablename__ = 'like'

    uid:str
    iid:int

    uid = db.Column(db.String(20),db.ForeignKey('user.uid'),nullable=False,primary_key=True)
    iid = db.Column(db.Integer,db.ForeignKey('user.uid'),nullable=False,primary_key=True)

@dataclass
class Comment(db.Model):
    __tablename__ = 'comment'

    cid:int
    pcid:int
    text:str
    time:str
    uid:str
    iid:int

    cid = db.Column(db.Integer,primary_key=True)
    pcid = db.Column(db.Integer,default = None)
    text = db.Column(db.String(50),nullable = False)
    time = db.Column(db.DateTime,nullable=False,default = datetime.now)

    uid = db.Column(db.String(20), db.ForeignKey('user.uid'), nullable=False)
    iid = db.Column(db.Integer,db.ForeignKey('img.iid'),nullable=False)
