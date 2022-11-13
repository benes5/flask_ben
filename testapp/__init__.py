from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bs5.db'


db = SQLAlchemy(app)
from .models import user, times, chats
from testapp.models.user import User
from testapp.models.times import Times
from testapp.models.chats import Chats

group_name_list = ["がんばり隊", "やるキング", "楽しみ隊"]

@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        flag = 0
        members = User.query.all()
        list_num = len(members)
        for member in members:
            if member.name == request.json["name"]:
                flag = 1
                return jsonify({
                    "access": "permit",
                    "group": member.group
                    })
                break
        if flag:
            random_num = random.randint(0,2)
            his_group = group_name_list[random_num]
            member = User(
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

            
            

@app.route("/api/setup/user",methods=["POST"])
def setup():
    if request.method == "POST":
        member = User(
            name="yamato",
            group="ss"
        )
        db.session.add(member)
        db.session.commit()
        return jsonify({"result": "success"})


@app.route("/api/settime", methods=["POST"])
def getTime():
    if request.method == "POST":
        print(request.json)
        times = Times(
            name= request.json["name"],
            time=request.json["time"]
        )
        db.session.add(times)
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

# @app.route("/api/chat")
# def chats():
    

if __name__ == '__main__':
    app.run(debug=True)