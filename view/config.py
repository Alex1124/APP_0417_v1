import os

# Define secret key to enable session
import secrets


class Config(object):
    TESTING = False
    
    
    REQUIREMENTS = os.path.join('env', 'requirements.txt')
    
    #資料庫設置
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:password@localhost:1433/Pet'      ###資料庫已建立 by  俐彤
    # SQLALCHEMY_DATABASE_URI = "mssql+pymssql://<帳號名稱>:<密碼>@<伺服器名稱>:1433/<資料庫名稱>"  ## 改成自己的資料庫連線設定
    # SQLALCHEMY_DATABASE_URI = "mssql+pymssql://sa:password@GB-205-A1:1433/Pet"  ##  GB-205-A1
    SECRET_KEY= str(secrets.token_hex())

    # 郵件設置
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'daniel07060706@gmail.com' 
    
    # 輸入你的google帳號的應用程式密碼 https://support.google.com/mail/answer/185833?hl=zh-Hant
    MAIL_PASSWORD = 'lnplzcjflaonfhjo'         
    #預設收件者
    MAIL_DEFAULT_SENDER = 'daniel07060706@gmail.com' 

class DevelopmentConfig(Config):

    #圖片上傳設定
    UPLOAD_FOLDER = os.path.join('static', 'upload')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}
  

    
