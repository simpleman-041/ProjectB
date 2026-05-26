from flask_sqlalchemy import SQLAlchemy

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        "{db}://{user}:{password}@{host}/{dbName}?charset=utf8".format(
            db = "mysql",
            user = "probc2026",
            password = "probc2026",
            host = "localhost",
            dbName = "probc2026"
        )
    db.init_app(app)
    return db

db = SQLAlchemy()
class ユーザ(db.Model):
    __tablename__ = "ユーザ"
    ID = db.Column(db.Integer, primary_key = True)
    氏名 = db.Column(db.String(50),nullable=False)
    所属ID = db.Column(
        db.Integer,
        db.ForeignKey("所属.所属ID"),
        nullable=False)
    電話番号 = db.Column(db.String(50))
    メールアドレス = db.Column(db.String(50))
class 所属(db.Model):
    __tablename__ = "所属"
    所属ID = db.Column(db.Integer, primary_key = True)
    所属名 = db.Column(db.String(50),nullable=False)
class 拾得物(db.Model):
    __tablename__ = "拾得物"
    ID = db.Column(db.Integer, primary_key = True)
    拾得物分類ID = db.Column(
        db.Integer,
        db.ForeignKey("拾得物分類.拾得物分類ID"),
        nullable=False)
    拾得場所 = db.Column(db.String(50),nullable=False)
    色 = db.Column(db.String(50),nullable=False)
    特徴 = db.Column(db.String(50),nullable=False)
class 拾得物分類(db.Model):
    __tablename__ = "拾得物分類"
    拾得物分類ID = db.Column(db.Integer, primary_key = True)
    分類名 = db.Column(db.String(50),nullable=False)
class 拾得物管理状況(db.Model):
    __tablename__ = "拾得物管理状況"
    ID = db.Column(db.Integer, primary_key = True)
    ユーザID = db.Column(
        db.Integer,
        db.ForeignKey("ユーザ.ID"),
        nullable=False)
    拾得物ID = db.Column(
        db.Integer,
        db.ForeignKey("拾得物.ID"),
        nullable=False)
    変更日時 = db.Column(db.DateTime)
    変更内容 = db.Column(db.String(50))
class 遺失物捜索依頼(db.Model):
    __tablename__ = "遺失物捜索依頼"
    ID = db.Column(db.Integer, primary_key = True)
    ユーザID = db.Column(
        db.Integer,
        db.ForeignKey("ユーザ.ID"),
        nullable=False)
    拾得物分類ID = db.Column(
        db.Integer,
        db.ForeignKey("拾得物分類.拾得物分類ID"),
        nullable=False)
    紛失場所 = db.Column(db.String(50))
    色 = db.Column(db.String(50))
    特徴 = db.Column(db.String(50))
    依頼日時 = db.Column(db.DateTime,nullable=False)
    
