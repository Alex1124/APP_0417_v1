
from flask import Flask, redirect, url_for ,request, render_template, Blueprint , jsonify, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy #https://docs.sqlalchemy.org/en/20/orm/
from flask_mail import Mail, Message
from flask_migrate import Migrate, upgrade



# 寫好的 py 檔案，在這邊引入
from view.recommend import recommend_page  
# 測試變數傳值
from view.variables_show_download_file import variables_test
# 圖表 plotly
from view.plotly_to_web import plotly_sample 
# config
from view.config import DevelopmentConfig
## 上傳圖片
from view.upload_display_image import upload_display_img 
# 登入註冊
from view.loginverify import login_page
# 貓咪狀況紀錄 與過敏原
from view.pethealth0410 import pethealth
# 首頁介紹
from view.index import index_page

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # 註冊 blueprint    #讓每個 view 資料夾中 py檔案 已經是 flask blueprint 物件，透過register_blueprint()引入到app
    app.register_blueprint(recommend_page)  #推薦頁面
    app.register_blueprint(variables_test)  #測試後端python 任何參數變數型態 傳入 前端 再到variable.html 寫好前端顯示方式
    app.register_blueprint(plotly_sample)  #測試plotly圖表 傳入 前端 
    app.register_blueprint(upload_display_img)  #測試 上傳圖片展示出來
    app.register_blueprint(login_page)  #登入註冊驗證
    app.register_blueprint(index_page)  #首頁
    app.register_blueprint(pethealth)  #貓咪狀況紀錄 與過敏原
    
    
     # 設定SQL連線與郵件等其他設定讓app知道
    app.config.from_object(DevelopmentConfig)
    
    mail = Mail(app)
    db = SQLAlchemy(app)

    return app


    # # 設定SQL連線與郵件等其他設定讓app知道
    # app.config.from_object(DevelopmentConfig)
    
    # mail = Mail(app)
    # # https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
    # db.init_app(app)
    # migrate = Migrate(app,db)
    # # db.init_app(app)
    # # db.create_all()
    # print(db)

    # return app
