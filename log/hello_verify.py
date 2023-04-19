
from flask import get_flashed_messages,Flask, flash,redirect, url_for ,request, render_template, Blueprint , jsonify, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy #https://docs.sqlalchemy.org/en/20/orm/
from flask_mail import Mail, Message
     
from view.config import DevelopmentConfig         
              

              
app = Flask(__name__)  
import secrets
# print(secrets.token_hex())
app.secret_key = str(secrets.token_hex())

@app.route('/',methods=['GET','POST'])
# 驗證碼確認頁面
def verify():     
    if request.method == 'POST':
        print("我post you")
        print("which names html have ?-->",request.values.keys())
        verification_code = request.values['verification_code']     
        print(verification_code)   
        
     
         

    ##這個網頁有問題，導致post 無法接收到 進入if 判斷 
    ## 因為把form 包裹到 body元素 
    # 還有加了奇怪的onclick 觸發到奇怪的網址去
    #導致整個無法post 超慘的= 口 + 
    # return render_template('loginverify.html')      
    return """<form method="post" action="">
                    Email驗證碼輸入:<input type="text" id="verify" name="verification_code" placeholder="Email驗證碼輸入"  required>
                    
                    <div class="tab"></div>
                    <button type="submit"  class="btn btn-primary"  >分析</button>

                
                </form>  
                
        """
                
                
if __name__ == "__main__":
    app.run(debug=True)