from flask import Flask, render_template, request, session
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint
from pathlib import Path


## 教學文章https://thinkinfi.com/upload-and-display-image-in-flask-python/

#*** Backend operation

# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER =  Path('static') / 'upload' #static\upload static\upload\cat2.jpg os.path.join('static', 'upload') 
# print(UPLOAD_FOLDER)
# print(os.path.join('static', 'upload'))

# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}
 
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder='templates', static_folder='static')
upload_display_img = Blueprint('upload_display_img', __name__, template_folder='templates', static_folder='static')
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


 
# Define secret key to enable session
import secrets
# print(secrets.token_hex())
app.secret_key = str(secrets.token_hex())
 
  
@upload_display_img.route('/upload')
def index():
    now = datetime.now()
    return render_template('hello.html', **locals())
 
@upload_display_img.route('/    ',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded_file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
 
        return render_template('hellov2.html')
 
@upload_display_img.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)
    # Display image in Flask application web page
    return render_template('hellov3.html', user_image = img_file_path)   # user_image 傳入HTML的變數名稱 = img_file_path 圖片地址
 
if __name__=='__main__':
    app.run(debug = True)