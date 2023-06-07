import dotenv
import os
from pymongo import MongoClient

import datetime as dt
from bson.objectid import ObjectId
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

# 로그인페이지(GET)
@app.route('/auth/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('index.html') #jsonify({'result':'success', 'msg': '이 요청은 GET!'}), 
    else :
        # 로그인페이지(POST)
        userid_receive = request.form['userid']
        userpw_receive = request.form['userpw']
        
        pw_hash = hashlib.sha256(userpw_receive.encode('utf-8')).hexdigest()

        doc = {"userid": userid_receive, "userpw": pw_hash}
        user = db.user.find_one(doc, {'_id':False})
        if user != None:
            session['loginUserId'] = user['userid']
            session['loginUserName'] = user['username']
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
def loginRegister():
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
    if user is not None:
        result = False #아이디 사용 못함
    else :
        result = True #아이디 사용 가능
        
    
    return jsonify({'result': result})

# 회원 탈퇴
@app.route('/auth/delete')
def deleteId():
    userid = session['loginUserId']

    doc = {'userid': userid}
    db.user.delete_one(doc)
    msg = '회원탈퇴 성공'
    
    return jsonify({'msg': msg})


# 게시판 목록
@app.route('/board/list', methods=['GET'])
def boardList():
    # title_receive = request.form['title_give']
    # all_favorites = list(db.favorites.find({},{'_id':False}))
    # return jsonify({'result':all_favorites})
    return render_template('main.html')


# 게시판 목록 불러오기
@app.route('/list', methods=['GET'])
def getList():
    # title_receive = request.form['title_give']
    all_favorites = list(db.favorites.find({}))
    for comment in all_favorites:
        comment['_id'] = str(comment['_id']) 

    return jsonify({'result':all_favorites})
    


# 게시판 조회 (상세페이지)
@app.route('/board/detail', methods=['GET'])
def boardDetail():
    num_receive = request.args.get('num')
    board_write = db.favorites.find_one({'_id':ObjectId(num_receive)}) # board_write 에 대한 dictionary {"userid": ~~, "address": ~~, "star": "4", ....}
    starNum = int(board_write['star']) # "4" > 숫자 4
    board_write['_id'] = str(board_write['_id'])
    return render_template('detail.html',context= board_write, context2=starNum)


# 게시판 조회 (상세페이지)
# @app.route('/board/detail', methods=['POST'])
# def boarddetail():
#     num_receive = request.form['num']
#     print("POST : ", num_receive)
#     user = db.favorites.find_one({'num':num_receive})
#     # print(type(user))
#     return render_template('datail.html',context=user)


# 게시판 글생성(POST) # 게시판 글생성(GET)
@app.route("/board/create", methods=["GET","POST"])
def boardCreate():
    if request.method == "GET":
        all_favorites = list(db.favorites.find({},{'_id':False}))
        return render_template('post.html')
    elif request.method == "POST":
        title_receive = request.form['title_give']
        address_receive = request.form['address_give']
        star_receive = request.form['star_give']
        comment_receive = request.form['comment_give']
        imgurl_receive = request.form['imgurl_give']
        userid = session.get('loginUserId')
        
        createday = dt.datetime.now().replace(microsecond=0)
        
        doc = {
            'title':title_receive,
            'address':address_receive,
            'star':star_receive,
            'comment':comment_receive,
            'imgurl':imgurl_receive,
            'date':createday,
            'userid' : userid
        }
        db.favorites.insert_one(doc) 

        return jsonify({'msg':'저장완료!'})

    
# 게시판 글수정
@app.route('/board/update', methods=['POST','GET']) 
def boardUpdate():
    
    if request.method == 'POST':
        num_receive = request.form['num_give']
        title_receive = request.form['title_give']
        address_receive = request.form['address_give']
        star_receive = request.form['star_give']
        comment_receive = request.form['comment_give']
        imgurl_receive = request.form['imgurl_give']

        db.favorites.update_one({'_id':ObjectId(num_receive)},{'$set': { 'title' : title_receive,
                                                                        'address' : address_receive,
                                                                        'star' : star_receive,
                                                                        'comment' : comment_receive,
                                                                        'imgurl' : imgurl_receive}})
        
        return jsonify({'result':'success', 'msg': '수정 완료'})

    if request.method == 'GET':
        num_receive = request.args.get('num') # ObjectId
        board_write = db.favorites.find_one({'_id':ObjectId(num_receive)})
        board_write['_id'] = str(board_write['_id'])
        starNum = int(board_write['star'])

        return render_template("update.html", context=board_write, context2=starNum)
    

# 게시판 글 삭제
@app.route('/board/delete', methods=['POST'])
def boardDelete():
    #boardNumber = request.form['boardNumber']
    boardNumber = request.get_json()
    
    db.favorites.delete_one({"_id":ObjectId(boardNumber['boardNumber'])})

    return jsonify({"result":'삭제완료!'})
    
if __name__ == '__main__':  
    app.run('0.0.0.0',port=5001,debug=True)