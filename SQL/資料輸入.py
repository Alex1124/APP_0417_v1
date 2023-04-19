import pandas as pd
import pymssql
from pathlib import Path

base = Path('SQL') 

#利用SQL檔建立資料庫以及所有表格 (以存放雲端SQL "專題資料庫20230329")
#更改以下 自己的資料庫資料 and data1~data9的檔案路徑

conn = pymssql.connect(server='localhost', user='sa', password='password', database='Pet')
cursor = conn.cursor()

#賣家
data1 = pd.read_csv(base / '賣家.csv')
for index, row in data1.iterrows(): 
    
    cursor.execute("INSERT INTO dbo.賣家(賣家代號,賣家名稱) VALUES('{}','{}')".format(row.賣家代號,row.賣家名稱))

#品牌
data2 = pd.read_csv(base / '品牌.csv')
for index,row in data2.iterrows():
    cursor.execute("INSERT INTO dbo.品牌(品牌代號,品牌名稱) VALUES('{}','{}')".format(row.品牌代碼,row.品牌名稱))

#通路
data3 = pd.read_csv(base / '通路.csv')
for index,row in data3.iterrows():
    cursor.execute("INSERT INTO dbo.通路(賣家代號,品牌代號) VALUES('{}','{}')".format(row.賣家代號,row.品牌代碼))
    



#會員
data4 = pd.read_csv(base / '會員紀錄.csv')
for index,row in data4.iterrows():
    cursor.execute("INSERT INTO dbo.會員(user_ID,姓名,帳號,密碼,信箱) VALUES('{}','{}','{}','{}','{}')".format(row.userID,row.姓名,row.帳號,row.密碼,row.信箱))    




#產品
data5 = pd.read_csv(base /  '產品.csv')
for index, row in data5.iterrows():
    cursor.execute("INSERT INTO dbo.產品(產品代碼,品牌代號,產品名稱,商品種類,適用年齡,圖片) VALUES('{}','{}','{}','{}','{}','{}')".format(row.產品代碼,row.品牌代碼,row.商品標題,row.商品種類,row.適用年齡,row.圖片))



#成分
data6 = pd.read_csv(base / '成分.csv')
for index, row in data6.iterrows():
    cursor.execute("INSERT INTO dbo.成分(產品代碼,成分1,成分2,成分3,成分4,成分5,成分6,成分7,成分8,成分9,成分10,成分11,成分12,成分13,成分14,成分15) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(row.產品代碼,row.成分1,row.成分2,row.成分3,row.成分4,row.成分5,row.成分6,row.成分7,row.成分8,row.成分9,row.成分10,row.成分11,row.成分12,row.成分13,row.成分14,row.成分15))




#貓咪狀況記錄 
#檢查重複 redata = data7.duplicated(['Pet_ID','紀錄日期'],keep=False)   print(redata[redata==True])
data7 = pd.read_csv(base / '貓咪狀況紀錄.csv')
for index,row in data7.iterrows():
    cursor.execute("INSERT INTO dbo.貓咪狀況記錄(user_ID,Pet_ID,Pet_Name,紀錄日期,毛孩生日,性別,體重,飯量,喝水量,小便次數,便便數量,時常抓癢,流眼淚,拉稀,嘔吐,頻尿) VALUES('{}','{}','{}','{}','{}','{}',{},{},{},{},{},{},{},{},{},{})".format(row.userID,row.Pet_ID,row.Pet_name,row.紀錄日期,row.毛孩生日,row.性別,row.體重,row.飯量,row.喝水量,row.小便次數,row.便便顆數,row.時常抓癢,row.流眼淚,row.拉稀,row.嘔吐,row.頻尿))


#價格表
data8 = pd.read_csv(base / '價格表.csv')
for index,row in data8.iterrows():
    cursor.execute("INSERT INTO dbo.價格表(賣家代號,產品代碼,價格) VALUES('{}','{}',{})".format(row.商品賣家,row.產品代碼,row.商品價格))


#過敏原
data9 = pd.read_csv(base / '過敏源.csv')
for index, row in data9.iterrows():
    cursor.execute("INSERT INTO dbo.過敏原(Pet_ID,紀錄日期,過敏原1,過敏原2,過敏原3,過敏原4,過敏原5,過敏原6,過敏原7,過敏原8,過敏原9,過敏原10) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(row.Pet_ID,row.紀錄日期,row.過敏原1,row.過敏原2,row.過敏原3,row.過敏原4,row.過敏原5,row.過敏原6,row.過敏原7,row.過敏原8,row.過敏原9,row.過敏原10))




conn.commit() 
conn.close()