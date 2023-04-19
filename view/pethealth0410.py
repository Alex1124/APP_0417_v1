import numpy as np
import pandas as pd
from datetime import datetime, date
from collections import OrderedDict
from pathlib import Path
import json
import logging
import re


from flask import Flask, redirect, url_for ,request ,render_template ,Blueprint , jsonify,session, current_app
from flask_sqlalchemy import SQLAlchemy
from view.config import DevelopmentConfig
from view.load_db import load_files,load_db
from view.my_log import my_logging
 
#  loggin 教學
# https://stackoverflow.com/questions/6386698/how-to-write-to-a-file-using-the-logging-python-module

#app = Flask(__name__)
#app.config.from_object(DevelopmentConfig)
app,db = load_db()
#db = SQLAlchemy(app)
pethealth = Blueprint('pethealth', __name__)

#loggin 紀錄
dev_logger = my_logging()
_, _,dataf,_ = load_files()
# with app.app_context():
#     app = current_app._get_current_object()

# def old_cat_db_process(app, sql1,sql2):
#     with app.app_context():
        
       
#         db.engine.execute(sql1)
#         dev_logger.info('貓咪狀況新增成功')
        
#         db.engine.execute(sql2)
#         dev_logger.info('新增過敏原成功')
#         print("db insert complete")



@pethealth.route('/pethealth_index',  methods=['GET', 'POST'])
def index():
    if session.get('logged_in') == True:
        print("/pethealth_index",request.method)

        return render_template('pethealth.html')
    else:
        return redirect( url_for('login_page.signup'))

# 貓咪健康狀況查詢 與推薦 /pethealth
@pethealth.route('/pethealth',  methods=['GET', 'POST'])
def pethealthfun():
    print("/pethealth",request.method)

    fullname = session.get('fullname')
    userid = session.get('userid')


    if request.method == 'POST':
  
        
        input_record = request.get_json()
        fullname = session.get('fullname')
        userid = session.get('userid')
        # data = json.dumps(input_record)
        dev_logger.info(f"get master input----->\n{input_record}")
        dict1 = dict()
        
        keys = ['username', 'petname','datepicker-bir', 'weight','datepicker-day', 'sex','appetite', 'water', 'pee', 'poop', 'scratch', 'tears', 'diarrhea', 'vomit', 'frequent','input-data', 'record-list-input']
        for i, key in enumerate(keys):
            dict1[key] = input_record[i]['value']
            
        dev_logger.info(f"dict1---->\n{dict1}")

        dict1['record-list-input'] = [ dict1['record-list-input'].split('、')[0].split(':')[-1] ] + dict1['record-list-input'].split('、')[1:-1]
        dev_logger.info(f"allegic--->{dict1['record-list-input']}")
        
        #尋找Pet_ID
        data = dataf[['user_ID','Pet_ID','Pet_Name','姓名','毛孩生日']].drop_duplicates(['user_ID','Pet_ID'],keep='first')
        mask = (data['user_ID'] == userid) & (data['Pet_Name'] == dict1['petname'])
        df = (data.loc[mask,['Pet_ID','毛孩生日']])
        
        

        if dict1['username'] == fullname:
            # 確認主人姓名有沒有打對，才執行
            print("不管新舊貓")


            #尋找Pet_ID
            # _, _,dataf,_ = load_files()
            # data = dataf[['user_ID','Pet_ID','Pet_Name','姓名','毛孩生日']].drop_duplicates(['user_ID','Pet_ID'],keep='first')
            # mask = (data['user_ID'] == userid) & (data['Pet_Name'] == dict1['petname'])
            # df = (data.loc[mask,['Pet_ID','毛孩生日']])
            
            if df.empty ==  True:
                print("新貓")
                try:
                    print("新貓")
                    sql1 = """select dbo.autopet()"""
                    with app.app_context():
                        Petid2 = db.engine.execute(sql1)
                    Petid2 = pd.DataFrame(Petid2).values[0][0]
                    print(Petid2)
                    sql2="""INSERT INTO dbo.貓咪狀況記錄(user_ID,Pet_ID,Pet_Name,紀錄日期,毛孩生日,性別,體重,飯量,喝水量,小便次數,便便數量,時常抓癢,流眼淚,拉稀,嘔吐,頻尿) 
                    VALUES('{}','{}','{}','{}','{}','{}',{},{},{},{},{},{},{},{},{},{})""".format(userid,Petid2, dict1['petname'], dict1['datepicker-day'],
                                                                                        dict1['datepicker-bir'],dict1['sex'], float(dict1['weight']), int(dict1['appetite']), int(dict1['water']),
                                                                                        int(dict1['pee']),
                                                                                        int(dict1['poop']), int(dict1['scratch']), int(dict1['tears']), int(dict1['diarrhea']), int(dict1['vomit']),
                                                                                        int(dict1['frequent']) )
                    # with app.app_context():
                    #     db.engine.execute(sql)
                    #     dev_logger.info('貓咪狀況新增成功')
                    
                    p = 10-len(dict1['record-list-input'])
                    # print(p)
                    for i in range(0,p):  
                        dict1['record-list-input'].append("")
                        
                    dict1['record-list-input'] = str(dict1['record-list-input'])
                    dict1['record-list-input'] = re.sub("\[|\]","",dict1['record-list-input'])
                    # print(dict1['record-list-input'])
                    
                    
                    sql3 = """INSERT INTO dbo.過敏原(Pet_ID,紀錄日期,過敏原1,過敏原2,過敏原3,過敏原4,過敏原5,過敏原6,過敏原7,過敏原8,過敏原9,過敏原10)
                    VALUES('{}','{}',{})""".format(Petid2,dict1['datepicker-day'],dict1['record-list-input'])
                    # print(sql2)
                    with app.app_context():
                        db.engine.execute(sql2)
                        dev_logger.info('貓咪狀況新增成功')
                        
                        db.engine.execute(sql3)
                        dev_logger.info('新增過敏原成功')
                        
                except Exception as e:
                    dev_logger.error(f"Catch an exception. - {e}", exc_info=True) 

                
            
            else:
                try:
                    print("救貓")
                    indv = list(df.index)[0]
                    Petid = df.at[indv,"Pet_ID"]
                    birth = df.at[indv,"毛孩生日"]            
                    # 新增貓咪紀錄狀況到資料庫
                    sql4="""INSERT INTO dbo.貓咪狀況記錄(user_ID,Pet_ID,Pet_Name,紀錄日期,毛孩生日,性別,體重,飯量,喝水量,小便次數,便便數量,時常抓癢,流眼淚,拉稀,嘔吐,頻尿) 
                    VALUES('{}','{}','{}','{}','{}','{}',{},{},{},{},{},{},{},{},{},{})""".format(userid,Petid, dict1['petname'], dict1['datepicker-day'],
                                                                                                birth,dict1['sex'], float(dict1['weight']), int(dict1['appetite']), int(dict1['water']),
                                                                                                int(dict1['pee']),
                                                                                                int(dict1['poop']), int(dict1['scratch']), int(dict1['tears']), int(dict1['diarrhea']), int(dict1['vomit']),
                                                                                                int(dict1['frequent']) )
                    print(sql4)
                    ################## 以下註解，就彈出視窗成功，還有將一些變數和程式碼分類到全域宣告處理 04/12
                    
                    
                    ########################################## 彈出視窗無法談的戰犯 嫌疑人 ###############
                    # with app.app_context():                 
                    #     db.engine.execute(sql4)
                    #     dev_logger.info('貓咪狀況新增成功')
                    ######################################## 彈出視窗無法談的戰犯 嫌疑人 ###############

                    # 新增過敏原到資料庫
                    p = 10-len(dict1['record-list-input'])
                    # print(p)
                    for i in range(0,p):  
                            dict1['record-list-input'].append("")
                            
                    dict1['record-list-input'] = str(dict1['record-list-input'])
                    dict1['record-list-input'] = re.sub("\[|\]","",dict1['record-list-input'])
                    print(dict1['record-list-input'])
                    sql5 = """INSERT INTO dbo.過敏原(Pet_ID,紀錄日期,過敏原1,過敏原2,過敏原3,過敏原4,過敏原5,過敏原6,過敏原7,過敏原8,過敏原9,過敏原10)
                    VALUES('{}','{}',{})""".format(Petid,dict1['datepicker-day'],dict1['record-list-input'])
                    print(sql5)
                    ########################################## 彈出視窗無法談的戰犯  ###############
                    with app.app_context():
                        db.engine.execute(sql4)
                        dev_logger.info('貓咪狀況新增成功')
                        
                        db.engine.execute(sql5)
                        dev_logger.info('新增過敏原成功')
                        print("db insert complete")
                    

                    
                    ########################################## 彈出視窗無法談的戰犯  ###############
                except Exception as e:
                    dev_logger.error(f"Catch an exception. - {e}", exc_info=True) 


                

        
            print(jsonify({"text":"新增成功"}))
            return jsonify({"text":"新增成功"})
        
        else:
            # 如果姓名輸入錯誤，則不做以上事情
            return jsonify({"text":"姓名輸入錯誤，請重新輸入"})
            # return redirect( url_for('pethealth.index'))
        
        


        
        






# ##如果是主程式，那就執行....
# if __name__ == '__main__':
#     # 執行 app.run() 函式，執行網頁伺服器的啟動動作
#     app.run(debug=True)
