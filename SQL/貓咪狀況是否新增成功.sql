/****** SSMS 中 SelectTopNRows 命令的指令碼  ******/
SELECT TOP (1000) [user_ID]
      ,[Pet_ID]
      ,[Pet_Name]
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
  FROM [Pet].[dbo].[貓咪狀況記錄]
  where [user_ID] = 'AF3'　and [Pet_ID] = 'CK10'