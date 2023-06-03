import dotenv
import os
from pymongo import MongoClient

dotenv.load_dotenv()

import certifi 
ca = certifi.where()
client = MongoClient(
    os.getenv("MONGO_URL"),
    tlsCAFile=ca,
)

db = client.dbsparta
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    #환영페이지 필요없으면
    #return redirect("/login")

# 로그인페이지(GET)
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        #title_receive = request.args.get('title_give') title_give라는 데이터를 가지고옴
        next = request.args.get('next', '') # login 후 이동할 페이지 지정
        return render_template('login.html') #jsonify({'result':'success', 'msg': '이 요청은 GET!'}), 
    else :
        # 로그인페이지(POST)
        #userid_receive = request.form['userid']
        #userpw_receive = request.form['userpw']
        
        doc = {"userid": "test", "userpw": "testpassword"}
        db.user.insert_one(doc)
        for i in db.user.find(): # 배포시 코드 지울 것
            print(i)
        return jsonify({'result':'success', 'msg': '이 요청은 POST!'})
    

# 회원가입(POST)
@app.route('/loginregister', methods=['POST'])
def loginregister():
    #userid_receive = request.form['userid']
    #userpw_receive = request.form['userpw']
    
    # 회원가입 db 저장
    #doc = {"userid": userid_receive, "userpw": userpw_receive}
    #db.user.insert_one(doc)
    
    return jsonify({'result':'success', 'msg': '이 요청은 POST!'})

# 아이디 중복확인(POST)
@app.route('/useridchek', methods=['POST'])
def useridchek():
    #title_receive = request.form['title_give']
    return jsonify({'result':'success', 'msg': '이 요청은 POST!'})


if __name__ == '__main__':  
    app.run('0.0.0.0',port=5001,debug=True)