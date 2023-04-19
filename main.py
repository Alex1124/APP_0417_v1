from app import create_app

# 網頁輸入月曆教學
# https://www.minwt.com/webdesign-dev/html/23247.html
    
#### 主程式 ####    
app = create_app()

if __name__ == '__main__': 
    app.run(debug=True)                                 