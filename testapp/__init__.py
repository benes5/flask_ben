from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bs5.db'


db = SQLAlchemy(app)
from .models import user, times, chats
from testapp.models.user import Accounts
from testapp.models.times import Times
from testapp.models.chats import Chats

group_name_list = ["がんばり隊", "やるキング", "楽しみ隊"]

@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        flag = True
        members = Accounts.query.all()
        # list_num = len(members)
        for member in members:
            if member.name == request.json["name"]:
                flag = False
                return jsonify({
                    "access": "permit",
                    "group": member.group
                    })
                break
        if flag:
            random_num = random.randint(0,2)
            his_group = group_name_list[random_num]
            member = Accounts(
                name= request.json["name"],
                group= his_group
            )
            db.session.add(member)
            db.session.commit()
            return jsonify({
                "access" : "new_user",
                "name":request.json["name"],
                "group": his_group
            })
@app.route("/api/test", methods=["POST"])
def test():
    if request.method == "POST":
        members = Accounts.query.all()
        print(members)
        return jsonify({"ok":"ok"})
            

@app.route("/api/setup/user",methods=["POST"])
def setup():
    if request.method == "POST":
        member = Accounts(
            name="yamato",
            group="ss"
        )
        db.session.add(member)
        db.session.commit()
        return jsonify({"result": "success"})


@app.route("/api/settime", methods=["POST"])
def getTime():
    if request.method == "POST":
        #timeの保存
        print(request.json)
        times = Times(
            name= request.json["name"],
            time=request.json["time"]
        )
        db.session.add(times)
        db.session.commit()
        #chatに送信
        his_name = request.json["name"]
        his_time = request.json["time"]
        comment = f"{his_name}さんは{his_time}で達成できました！"
        members = Accounts.query.all()
        his_group = ""
        for member in members:
            if member.name == request.json["name"]:
                his_group = member.group
                break   
        new_chat = Chats(
            group= his_group,
            name= request.json["name"],
            text= comment
        )
        db.session.add(new_chat)
        db.session.commit()
        return jsonify({"result": "success"})


@app.route("/api/lists", methods=["GET"])
def time_get():
    if request.method == "GET":
        time_list = Times.query.all()
        print(time_list)
        objs = []
        for time in time_list:
            if time.name == "kohei":
                print(type(time.created_at.year))
                print((time.created_at.year))
                obj = {
                    "year": time.created_at.year,
                    "month": time.created_at.month,
                    "day": time.created_at.day,
                    "time": time.time
                }
                objs.append(obj)
        
        return jsonify({"result": objs})

@app.route("/api/chat/add",methods=["POST"])
def add_chats():
    if request.method == "POST":
        members = Accounts.query.all()
        his_group = ""
        for member in members:
            if member.name == request.json["name"]:
                his_group = member.group
                break     
        new_chat = Chats(
            group= his_group,
            name= request.json["name"],
            text= request.json["text"]
        )
        db.session.add(new_chat)
        db.session.commit()
        return jsonify({"result":"send_complete"})


@app.route("/api/chat/get",methods=["POST"])
def get_chats():
    members = Accounts.query.all()
    his_group = ""
    group_chat=[]
    for member in members:
        if member.name == request.json["name"]:
            his_group = member.group        
    all_chats = Chats.query.all()
    for one_chat in all_chats:
        if one_chat.group == his_group:
            obj = {
                "name": one_chat.name,
                "text": one_chat.text
            }
            group_chat.append(obj)
    return jsonify({"chats": group_chat})
            

# @app.route("/api/network",methods=["POST"])
#     if request.method == "POST":

if __name__ == '__main__':
    app.run(debug=True)