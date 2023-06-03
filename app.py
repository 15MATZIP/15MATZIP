import dotenv
import os
from pymongo import MongoClient

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)

# import jwt


# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
#import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib

dotenv.load_dotenv()

import certifi 
ca = certifi.where()
client = MongoClient(
    os.getenv("MONGO_URL"),
    tlsCAFile=ca,
)

db = client.dbsparta
from flask import Flask, render_template, request, jsonify, redirect, url_for
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
        
        doc = {"userid": "adsasdasda", "userpw": "efewf"}
        db.user.insert_one(doc)
        
        return jsonify({'result':'success', 'msg': '이 요청은 POST!'})
    

# 회원가입(POST)
@app.route('/loginregister', methods=['POST'])
def loginregister():
    userid_receive = request.form['userid']
    userpw_receive = request.form['userpw']
    
    pw_hash = hashlib.sha256(userpw_receive.encode('utf-8')).hexdigest()


    # 회원가입 db 저장
    doc = {"userid": userid_receive, "userpw": pw_hash}
    db.user.insert_one(doc)
    
    return redirect(url_for('login'))

# 아이디 중복확인(POST)
@app.route('/useridchek', methods=['POST'])
def useridchek():
    #title_receive = request.form['title_give']
    return jsonify({'result':'success', 'msg': '이 요청은 POST!'})


if __name__ == '__main__':  
    app.run('0.0.0.0',port=5001,debug=True)