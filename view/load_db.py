
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from pathlib import Path
from collections import OrderedDict

# main 主程式使用這行
from view.config import DevelopmentConfig
from view.my_log import my_logging
# 在這邊測試使用這行
# from config import DevelopmentConfig
dev_logger = my_logging() 
 
def load_db(): 
    """
    要先到view/config.py 中 設定 DevelopmentConfig 中的 
    資料庫連線設定 SQLALCHEMY_DATABASE_URI = 改成自己的連線設定
    """
    
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db = SQLAlchemy(app)
    # with app.app_context():
    #     db.init_app(app)


    return app, db


def load_files():
    """#### 取得df_product產品表, df_ingredients成分表, df_cat_health貓咪狀況記錄, df_allergic_agent過敏原表"""
    try:
        app, db = load_db()
    except Exception as e:
        dev_logger.error(f"請先到config.py設定資料庫連線與其他設定!!\nCatch an exception.{e}", exc_info=True)



    with app.app_context():

        try:
            # 要先執行預存程序
            sql ="""select * from ##product_price"""        #產品索引表
            product = db.engine.execute(sql)
            df_product = pd.DataFrame(product)

            sql_2 ="""select * from [dbo].[成分]""" 
            ingredients = db.engine.execute(sql_2)
            df_ingredients = pd.DataFrame(ingredients)

            sql_3 ="""exec create_user_catcondition"""
            cat_health = db.engine.execute(sql_3)
            df_cat_health = pd.DataFrame(cat_health)

            sql_4 ="""exec create_user_catcondition_allergic_agent"""
            allergic_agent = db.engine.execute(sql_4)
            df_allergic_agent = pd.DataFrame(allergic_agent)

            # print(df_product)
            # print(df_ingredients)
            # print(df_cat_health)
            # print(df_allergic_agent) 
            
            return df_product, df_ingredients, df_cat_health, df_allergic_agent
        except Exception as e:
            dev_logger.error(f"請先執行資料的預存程序!!\nCatch an exception.{e}", exc_info=True)

    
    


