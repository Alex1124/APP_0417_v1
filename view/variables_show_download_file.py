from flask import Flask
from flask import render_template
from datetime import datetime
from flask import url_for, redirect, Blueprint, send_from_directory
import os

# https://www.delftstack.com/zh-tw/howto/python-flask/flask-url_for/
# https://www.runoob.com/html/html-links.html



# 宣告 Blueprint 物件 名稱取的有意義比較好
variables_test = Blueprint(name='variables_test', import_name= __name__)


# @宣告的blueprint物件變數名稱.route('/variable')
@variables_test.route('/variable')
def variables():
    user = {'id':'20230305', 'name':'小明', 'city':'台南', 'score':95}
    language = ['Java', 'Python', 'c#']

    list1 = range(1, 6)
    
    user1 = {'id':'20230305', 'name':'小明', 'city':'台南', 'score':95}
    user2 = {'id':'20230306', 'name':'Lisa', 'city':'台北', 'score':75}
    user3 = {'id':'20230307', 'name':'小花', 'city':'台中', 'score':85}
    users = [user1, user2, user3]

    return render_template('variable.html', **locals())

 
## 測試 download 執行

@variables_test.route('/download')
def index():

    filename='cat2.jpg'
    return send_from_directory('static/upload', filename, as_attachment=True)

 
