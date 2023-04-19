from flask import Flask, jsonify, render_template, Blueprint ,request, redirect, url_for, flash ,session ,current_app
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import random
import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash


# 登入驗證登出教學
# https://ithelp.ithome.com.tw/articles/10273551
# https://stackoverflow.com/questions/17972020/how-to-execute-raw-sql-in-flask-sqlalchemy-app
# 郵件教學
# https://hackmd.io/@shaoeChen/BytvGKs4M

# app = Flask(__name__)
login_page = Blueprint('login_page',__name__)
 
##### app.config 宣告，都在專題APP/view/config.py 裡面 這邊要使用時候只要引入就可
# DevelopmentConfig 開發設置的設定
from view.config import DevelopmentConfig
# app.config.from_object(DevelopmentConfig)
from view.my_log import my_logging
from view.load_db import load_db

mail = Mail() 
app, db = load_db()
# db = SQLAlchemy()
# db.init_app(current_app)
dev_logger = my_logging()


# 註冊表單
def save_to_database(fullname ,account, email, password):
    with app.app_context():
        sql1 = f"select * from [dbo].[會員] WHERE [信箱] = '{email}' or [帳號]='{account}'"
        member_check=db.engine.execute(sql1)
       
        member_check = pd.DataFrame(member_check)
        print("--------?",member_check)
    if member_check.empty == True:
        with app.app_context():
            sql2 = '''
                    DECLARE @result nvarchar(50);
                    DECLARE @new_id int = COALESCE((SELECT MAX(CAST(SUBSTRING(user_ID, 3, 5) AS int)) FROM [dbo].[會員]), 0) + 1;
                    SET @result = 'AF' + RIGHT('0' + CAST(@new_id AS nvarchar(5)), 5);
                    select @result;'''
            sid = db.engine.execute(sql2)
            sid = pd.DataFrame(sid).values[0][0]
            print(sid)
            sql3 = f"INSERT INTO [dbo].[會員] ([user_ID], [姓名], [帳號], [密碼], [信箱]) VALUES ( '{sid}' ,'{fullname}' ,'{account}', '{password}','{email}')"
            # sql =f"select * from [Pet].[dbo].[Table_1]"
            db.engine.execute(sql3)
            dev_logger.info("save success")


    else:
        return redirect( url_for('login_page.signup'))
    
def confirm_member(account , password):
    with app.app_context():
        sql = f"select * from [dbo].[會員] WHERE [帳號]='{account}' and [密碼] = '{password}'"
        result= db.engine.execute(sql,account , password)
        result = pd.DataFrame(result)
        dev_logger.info(result)
        if result.empty == False:
            session['userid']=result.values[0][0]
            session['fullname']=result.values[0][1]
        
        #  check_password_hash(user['password'], password)
        # print(f"confirm ? {result}")
    return result.empty
    # return db.engine.execute(sql,account , password)


@login_page.route('/verify',methods=['GET','POST'])
# 驗證碼確認頁面
def verify():

    if request.method == 'POST':
        print("我post you")
        dev_logger.info(f"which names html have ?-->\n{request.values.keys()}")
        verification_code = request.values['verification_code']
        dev_logger.info(f"{verification_code}, {session.get('V_code')} , {session.get('V_code') == verification_code}" )    
        
        
        # 檢查驗證碼是否正確，這裡使用假的函數代替
        if session.get('V_code') == verification_code:
            flash('驗證碼正確，註冊成功！')
            dev_logger.info("驗證碼正確")
            #寫入資料庫
            
            save_to_database(session['fullname'], session['account'], session['email'],session['password'])
            return redirect(url_for('login_page.signup'))
        else:
            flash('驗證碼錯誤，請重新輸入。')
            dev_logger.info("驗證碼錯誤")
            
            return render_template('login.html')
        
    return render_template('loginverify.html')


@login_page.route('/signup',methods=['GET','POST'])
# 會員註冊+登入 頁面
def signup():
    # with app.app_context():
    #     # OK
    #     sql = f"select * from 會員"
    #     result =db.engine.execute(sql)
    #     print(pd.DataFrame(result))

    # with current_app.app_context():
    #     sql = f"select * from 會員"
    #     result =db.engine.execute(sql)
    #     print(pd.DataFrame(result))


    if request.method == 'POST' :
        dev_logger.info(f"現在app有哪些{session.keys()}")
        dev_logger.info(f"signup post for what keys? { request.values.keys()}")

        



        if len(request.values.keys() ) == 5:
            # 註冊階段
            session['fullname'] = request.form['fullname']
            session['account'] =  request.form['account']
            session['password'] = request.form['password']
            session['email'] = request.form['email']
            #產生6位數字驗證碼數字驗證碼(100000~999999)
            session['V_code'] = str( random.randint(100000, 999999) )
            # session['V_code'] = str(111111)
            #下面是使用者email 若email是空的會寄信給預設收件者
            with current_app.app_context():

                dev_logger.info(f"現在要寄信的郵箱是{session['email']}")
                email = session['email']
                message = Message('註冊驗證碼', recipients=[email])
                message.body = f'你的驗證碼是 {session["V_code"]}'
                mail.send(message)
                dev_logger.info("郵件已傳送")  
                return redirect( url_for('login_page.verify'))
            
        if len(request.values.keys() ) == 2:
            # 登入階段

                account = session['account'] = request.form['account']
                password = session['password'] = request.form['password']

                dev_logger.info(f"使用者輸入的帳密{account} {password}")
                if confirm_member(account , password) == False: 
                    # 確認是否為會員
                    session['logged_in']=True
                    # 儲存所有會員的資料 session 會員姓名等
                    return redirect(url_for('login_page.index'))
                    return render_template('login.html', message="登入成功！<script>alert('登入成功！');</script>") 
                
                else:
                    # 確認是否為會員
                    session['logged_in']=False
                    return redirect(url_for('login_page.signup'))
                    return render_template('login.html', message="登入失敗！<script>alert('登入失敗！');</script>") 
            # 
            
            
    return render_template('login.html')

@login_page.route('/index', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')



@login_page.route('/logout',methods=['GET','POST'])
def logout():
    session['logged_in']=False
    return render_template('index.html')        

##以下JS用
@login_page.route('/check_email', methods=['POST'])
def check_email():
    email = request.form['username2']

    # 查詢資料庫中是否存在該 Email
  
    sql = f"SELECT * FROM users WHERE email = {email}"
    db.execute(sql)
    result = db.fetchone()

    # 返回結果 
    if result:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})

@login_page.route('/check_account', methods=['POST'])
def check_account():
    account = request.form['username1']

    # 查詢資料庫中是否存在該 account
  
    sql = f"SELECT * FROM users WHERE email = {account}"
    db.execute(sql)
    result = db.fetchone()

    # 返回結果
    if result:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})
