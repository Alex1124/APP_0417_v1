import numpy as np
import pandas as pd
from datetime import datetime, date
from collections import OrderedDict
from pathlib import Path
import json
import logging

from flask import Flask, redirect, url_for ,request ,render_template ,Blueprint , jsonify
from flask_sqlalchemy import SQLAlchemy
from view.config import DevelopmentConfig
 
#  loggin 教學
# https://stackoverflow.com/questions/6386698/how-to-write-to-a-file-using-the-logging-python-module

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
# pethealth = Blueprint('pethealth', __name__)

#loggin 紀錄
dev_logger: logging.Logger = logging.getLogger(name='dev')
dev_logger.setLevel(logging.DEBUG)

handler: logging.StreamHandler = logging.StreamHandler()
filepath : logging.FileHandler = logging.FileHandler(Path('log') / 'logging.txt', mode='a', encoding='utf-8')
formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

filepath.setLevel(logging.DEBUG)
filepath.setFormatter(formatter)

handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

dev_logger.addHandler(handler)
dev_logger.addHandler(filepath)

@app.route('/',  methods=['GET', 'POST'])
def index():
    print("/",request.method)

    return render_template('pethealth.html')

# 貓咪健康狀況查詢 與推薦 /health
@app.route('/pethealth',  methods=['GET', 'POST'])
def pethealth():
    print("/pethealth",request.method)
    if request.method == 'POST':
        # input_record = request.values['name']
        
        input_record = request.get_json()
        # data = json.dumps(input_record)
        print("----->",input_record)
        dict1 = dict()
        
        keys = ['username', 'petname','date', 'sex', 'age', 'weight', 'appetite', 
                'water', 'pee', 'poop', 'scratch', 'tears', 'diarrhea', 'vomit', 'frequent', 
                'input-data', 'allergen', 'record-list-input']
        for i, key in enumerate(keys):
            dict1[key] = input_record[i]['value']
            
        dev_logger.info(f"dict1---->{dict1}")

        dict1['allergen'] = [ dict1['allergen'].split('、')[0].split(':')[-1] ] + dict1['allergen'].split('、')[1:-1]
        dev_logger.info(f"allegic--->{dict1['allergen']}")
        # 新增資料到資料庫
        sql="""INSERT INTO dbo.貓咪狀況記錄(user_ID,Pet_ID,Pet_Name,紀錄日期,毛孩生日,性別,體重,飯量,喝水量,小便次數,便便數量,時常抓癢,流眼淚,拉稀,嘔吐,頻尿) 
        VALUES('{}','{}','{}','{}','{}','{}',{},{},{},{},{},{},{},{},{},{})""".format('AF3','CK10', dict1['petname'], dict1['date'],
                                                                                      '2015-01-01',dict1['sex'], float('5.9'), int(dict1['appetite']), int(dict1['water']),
                                                                                      int(dict1['pee']),
                                                                                      int(dict1['poop']), int(dict1['scratch']), int(dict1['tears']), int(dict1['diarrhea']), int(dict1['vomit']),
                                                                                      int(dict1['frequent']) )
        db.engine.execute(sql)
        dev_logger.info("db insert complete")
        
        dev_logger.info(f'jsonify----->{jsonify(dict1)}')  #<Response 385 bytes [200 OK]>
        return jsonify(dict1)
        
    




##如果是主程式，那就執行....
if __name__ == '__main__':
    # 執行 app.run() 函式，執行網頁伺服器的啟動動作
    app.run(debug=True)
