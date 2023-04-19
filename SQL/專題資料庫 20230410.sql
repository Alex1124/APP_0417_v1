--CREATE DATABASE Pet
USE Pet

CREATE TABLE 賣家 (
                賣家代號 NVARCHAR(2) NOT NULL,
                賣家名稱 NVARCHAR(15) NOT NULL,
                  PRIMARY KEY (賣家代號)
)

CREATE TABLE 品牌 (
                品牌代號 NVARCHAR(5) NOT NULL,
                品牌名稱 NVARCHAR(20) NOT NULL,
                  PRIMARY KEY (品牌代號)
)


CREATE TABLE 通路 (
                品牌代號 NVARCHAR(5) NOT NULL,
                賣家代號 NVARCHAR(2) NOT NULL,
                  PRIMARY KEY (品牌代號, 賣家代號)
)




CREATE TABLE 產品 (
                產品代碼 NVARCHAR(6) NOT NULL,
                品牌代號 NVARCHAR(5) NOT NULL,
                產品名稱 NVARCHAR(MAX) NOT NULL,
                商品種類 NVARCHAR(4) NOT NULL,
                適用年齡 NVARCHAR(3) NOT NULL,
                圖片 NVARCHAR(50) NOT NULL,
                  PRIMARY KEY (產品代碼)
)

CREATE TABLE 成分 (
                產品代碼 NVARCHAR(6) NOT NULL,
                成分1 NVARCHAR(50),
                成分2 NVARCHAR(50),
                成分3 NVARCHAR(50),
                成分4 NVARCHAR(50),
                成分5 NVARCHAR(50),
                成分6 NVARCHAR(50),
                成分7 NVARCHAR(50),
                成分8 NVARCHAR(50),
                成分9 NVARCHAR(50),
                成分10 NVARCHAR(50),
                成分11 NVARCHAR(50),
                成分12 NVARCHAR(50),
                成分13 NVARCHAR(50),
                成分14 NVARCHAR(50),
                成分15 NVARCHAR(50),
                  PRIMARY KEY (產品代碼)
)

CREATE TABLE 會員 (
                user_ID NVARCHAR(5) NOT NULL,
                姓名 NVARCHAR(15) NOT NULL,
                帳號 NVARCHAR(15) NOT NULL,
                密碼 NVARCHAR(15) NOT NULL,
                信箱 NVARCHAR(MAX) NOT NULL,
                  PRIMARY KEY (user_ID)
)

CREATE TABLE 貓咪狀況記錄 (
                user_ID NVARCHAR(5) NOT NULL,
                Pet_ID NVARCHAR(5) NOT NULL,
                Pet_Name NVARCHAR(30) NOT NULL,
                紀錄日期 DATE NOT NULL ,
                毛孩生日 DATE NOT NULL,
                性別 NVARCHAR(2) NOT NULL,
                體重 DECIMAL(6,2),
                飯量 TINYINT,
                喝水量 TINYINT,
                小便次數 TINYINT,
                便便數量 TINYINT,
                時常抓癢 TINYINT,
                流眼淚 TINYINT,
                拉稀 TINYINT,
                嘔吐 TINYINT,
                頻尿 TINYINT,
                PRIMARY KEY (Pet_ID,紀錄日期)
)

CREATE TABLE 過敏原 (
                Pet_ID NVARCHAR(5) NOT NULL,
                紀錄日期 DATE NOT NULL,
                過敏原1 NVARCHAR(7),
                過敏原2 NVARCHAR(7),
                過敏原3 NVARCHAR(7),
                過敏原4 NVARCHAR(7),
                過敏原5 NVARCHAR(7),
                過敏原6 NVARCHAR(7),
                過敏原7 NVARCHAR(7),
                過敏原8 NVARCHAR(7),
                過敏原9 NVARCHAR(7),
                過敏原10 VARCHAR(7),
                PRIMARY KEY (Pet_ID,紀錄日期)
)

CREATE TABLE 價格表(
                    賣家代號 NVARCHAR(2) NOT NULL,
                    產品代碼 NVARCHAR(6) NOT NULL,
                    價格 INT NOT NULL,
                    PRIMARY KEY(賣家代號,產品代碼)
                   )


ALTER TABLE 通路 ADD  
FOREIGN KEY (賣家代號)
REFERENCES 賣家 (賣家代號)
ON DELETE NO ACTION
ON UPDATE NO ACTION


ALTER TABLE 通路 ADD  
FOREIGN KEY (品牌代號)
REFERENCES 品牌 (品牌代號)
ON DELETE NO ACTION
ON UPDATE NO ACTION



ALTER TABLE 產品 ADD  
FOREIGN KEY (品牌代號)
REFERENCES 品牌 (品牌代號)
ON DELETE NO ACTION
ON UPDATE NO ACTION



ALTER TABLE 成分 ADD  
FOREIGN KEY (產品代碼)
REFERENCES 產品 (產品代碼)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE 貓咪狀況記錄 ADD  
FOREIGN KEY (user_ID)
REFERENCES 會員 (user_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE 過敏原 ADD  
FOREIGN KEY (Pet_ID,紀錄日期)
REFERENCES 貓咪狀況記錄 (Pet_ID,紀錄日期)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE 價格表 ADD
FOREIGN KEY (賣家代號)
REFERENCES 賣家 (賣家代號)

ALTER TABLE 價格表 ADD
FOREIGN KEY (產品代碼)
REFERENCES 產品 (產品代碼)