use Pet
go

CREATE OR ALTER PROCEDURE create_user_catcondition
AS BEGIN
	-- 因為使用者輸入，不會輸入任何表的ID  使用者姓名  有哪隻貓名 有哪些過敏原 
	--會員 關聯 貓咪狀況記錄 關聯 過敏原表\
	--方便 查詢 貓咪ID & 最新紀錄日期 & 過敏原 是 哪隻貓?????
    SELECT	a.[user_ID]
			,c.[Pet_ID]
			,c.[Pet_Name]
			,a.姓名
			      ,[紀錄日期]
      ,[毛孩生日]
      ,[性別]
      ,[體重]
      ,[飯量]
      ,[喝水量]
      ,[小便次數]
      ,[便便數量]
      ,[時常抓癢]
      ,[流眼淚]
      ,[拉稀]
      ,[嘔吐]
      ,[頻尿]
	INTO #user_cathealth_     
	FROM [Pet].[dbo].[貓咪狀況記錄] c   join  [dbo].[會員] a on c.user_ID = a.user_ID

	SELECT  * from #user_cathealth_;   
END
go

use Pet
exec create_user_catcondition;
