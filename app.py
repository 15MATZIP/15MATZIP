import dotenv
import os
from pymongo import MongoClient


import hashlib

dotenv.load_dotenv()

import certifi 
ca = certifi.where()
client = MongoClient(
    os.getenv("MONGO_URL"),
    tlsCAFile=ca,
)

db = client.dbsparta
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
app = Flask(__name__)
app.secret_key = os.getenv("OurKey") #가려야함

# 시작 페이지
@app.route('/')
def home():

    return redirect("/auth/login")

    #return render_template('index.html')
    #환영페이지 필요없으면
    #return redirect("/login")

# 로그인페이지(GET)
@app.route('/auth/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        #title_receive = request.args.get('title_give') title_give라는 데이터를 가지고옴
        next = request.args.get('next', '') # login 후 이동할 페이지 지정

        user_list = list(db.user.find({}))
        if len(user_list) == 0:
            print('없음')
        else :
            for i in user_list:
                print(i)

        return render_template('index.html') #jsonify({'result':'success', 'msg': '이 요청은 GET!'}), 
    else :
        # 로그인페이지(POST)
        userid_receive = request.form['userid']
        userpw_receive = request.form['userpw']
        
        pw_hash = hashlib.sha256(userpw_receive.encode('utf-8')).hexdigest()

        doc = {"userid": userid_receive, "userpw": pw_hash}
        user = db.user.find_one(doc, {'_id':False})
        print("넘어왔나?", user)
        if user != None:
            session['loginUserId'] = user['userid']
            print(session.get('loginUserId'))    #>> 세션 저장 확인
            result = True
            msg = f"{user['username']}님 환영합니다"
        else:
            result = False
            msg = "로그인에 실패하였습니다."
        return jsonify({"result": result, "msg": msg})
    
# 로그아웃
@app.route('/auth/logout')
def logout():
    if session.get('loginUserId'):
        isLogout = True

        session.clear()

        msg = '로그아웃 성공'

    else:
        isLogout = False

        msg = "로그아웃 실패"
        
    return jsonify({"result": isLogout, "msg":msg})


# 회원가입(POST)
@app.route('/auth/register', methods=['POST'])
def loginregister():
    userid_receive = request.form['userid']
    userpw_receive = request.form['userpw']
    username_receive = request.form['username']
    
    pw_hash = hashlib.sha256(userpw_receive.encode('utf-8')).hexdigest()

    # 회원가입 db 저장
    doc = { 
        "userid": userid_receive,
        "userpw": pw_hash, 
        "username":username_receive
        }
    db.user.insert_one(doc)
    return jsonify({'result':'success', 'msg': '가입 완료!'})



# 아이디 중복확인(POST)
@app.route('/auth/useridcheck', methods=['POST'])
def useridchek():
    userid_receive = request.form['userid']
    user = db.user.find_one({'userid': userid_receive})
    print(user)
    if user is not None:
        result = False
    else :
        result = True
        
    
    return jsonify({'result': result})

# 회원 탈퇴
@app.route('/auth/delete')
def deleteId():
    userid = session['loginUserId']

    doc = {'userid': userid}
    db.user.delete_one(doc)
    msg = '회원탈퇴 성공'
    
    return jsonify({'msg': msg})


if __name__ == '__main__':  
    app.run('0.0.0.0',port=5001,debug=True)