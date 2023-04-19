from flask import Flask, render_template, request, session
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint
from pathlib import Path


# static\upload static\upload\cat2.jpg os.path.join('static', 'upload')
UPLOAD_FOLDER = Path('static') / 'upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}
index_page = Blueprint('index_page',  __name__)


@index_page.route('/')
def first():

    print(session.get('fullname'))
    print(session.get('userid'))
    return render_template('index.html', **locals())
