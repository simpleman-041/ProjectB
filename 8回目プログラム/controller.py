from flask import render_template, jsonify
from sqlalchemy import func
from model import db, ユーザ, 所属, 拾得物, 拾得物分類, 拾得物管理状況

def top():
    return render_template("top.html")

def get_json(data):
    if data == "user":
        return jsonify(get_user_list())
    elif data == "item":
        return jsonify(get_item_list())
    elif data == "category":
        return jsonify(get_category_list())
    elif data == "dept":
        return jsonify(get_dept_list())

def get_dept_list():
    data = db.session.query(所属).all()
    obj = []
    for i in data:
        obj.append({
            "所属ID":i.ID,
            "所属分類":i.所属分類,
            "所属名":i.所属名, 
            })
    return(obj)

def get_user_list():
    data = db.session.query(ユーザ,所属).filter(ユーザ.所属ID==所属.ID).all()
    obj = []
    for i,j in data:
        obj.append({
            "ID":i.ID,
            "氏名":i.氏名,
            "電話番号":i.電話番号,
            "メールアドレス":i.メールアドレス,
            "住所":i.住所,
            "所属分類":j.所属分類,
            "所属名":j.所属名, 
            })
    return(obj)

def get_item_list(key=""):
    lastdt = db.session.query(
        拾得物管理状況.拾得物ID.label("oid"),
        func.max(拾得物管理状況.変更日時).label("last")
    ).group_by(
        拾得物管理状況.拾得物ID
    ).subquery()
    tmp = db.session.query(
        拾得物管理状況, 
        拾得物, 
        拾得物分類, 
        ユーザ, 
        所属
    ).filter(
        拾得物管理状況.拾得物ID==拾得物.ID
    ).filter(
        拾得物.拾得物分類ID==拾得物分類.ID
    ).filter(
        拾得物管理状況.ユーザID==ユーザ.ID
    ).filter(
        ユーザ.所属ID==所属.ID
    ).filter(
        拾得物管理状況.変更日時==lastdt.c.last
    ).filter(
        拾得物管理状況.拾得物ID==lastdt.c.oid
    )
    if key == "":
        data = tmp.all()
    else:
        data = tmp.filter(拾得物分類.物品名.contains(key)).all()
    obj = []
    for i,j,k,l,m in data:
        obj.append({
            "大分類":k.大分類,
            "物品名":k.物品名,
            "貴重品":k.貴重品,
            "拾得物ID":j.ID,
            "拾得場所":j.拾得場所,
            "色":j.色,
            "特徴":j.特徴,
            "画像":j.画像,
            "拾得物管理状況ID":i.ID,
            "変更日時":i.変更日時,
            "変更内容":i.変更内容,
            "氏名":l.氏名,
            "所属名":m.所属名, 
            })
    return(obj)

def get_category_list():
    data = db.session.query(拾得物分類).all()
    obj = []
    for i in data:
        obj.append({
            "ID":i.ID,
            "大分類":i.大分類,
            "物品名":i.物品名,
            "頭１":i.頭１,
            "頭２":i.頭２,
            "五十音":i.五十音,
            "貴重品":i.貴重品, 
            })
    return(obj)

def search_item(k):
    j = get_item_list(k)
    return render_template("item_list.html", j=j, n=len(j))

def get_item_detail(id):
    data = db.session.query(拾得物管理状況,ユーザ).filter(拾得物管理状況.ユーザID==ユーザ.ID).filter(拾得物管理状況.拾得物ID==id)
    list = []
    for i,j in data:
        list.append({
            "変更日時":i.変更日時,
            "変更内容":i.変更内容,
            "氏名":j.氏名,
        })
    result = db.session.query(拾得物,拾得物分類).filter(拾得物.拾得物分類ID==拾得物分類.ID).filter(拾得物.ID==id).first()
    if result is None:
        return "指定された拾得物は存在しません"
    i,j = result
    if i.画像 is None:
        i.画像 = ""
    d = {
        "大分類":j.大分類,
        "物品名":j.物品名,
        "拾得場所":i.拾得場所,
        "色":i.色,
        "特徴":i.特徴,
        "画像":i.画像, 
        "変更履歴":list, 
        "id":id
        }
    return render_template("item_detail.html", d=d, u=get_user_list())
