/****** SSMS 中 SelectTopNRows 命令的指令碼  ******/
use pet
go

SELECT a.[user_ID]
      ,c.[Pet_ID]
      ,c.[Pet_Name]
	  ,a.姓名
into #user_cathealth     
FROM [Pet].[dbo].[貓咪狀況記錄] c inner join  [dbo].[會員] a on c.user_ID = a.user_ID
go

select * from #user_cathealth uc inner join [dbo].[過敏原] aa on uc.Pet_ID = aa.Pet_ID;
go


CREATE OR ALTER PROCEDURE create_user_catcondition_allergic_agent

AS BEGIN
	-- 因為使用者輸入，不會輸入任何表的ID  使用者姓名  有哪隻貓名 有哪些過敏原 
	--會員 關聯 貓咪狀況記錄 關聯 過敏原表\
	--方便 查詢 貓咪ID & 最新紀錄日期 & 過敏原 是 哪隻貓?????
    SELECT	a.[user_ID]
			,c.[Pet_ID]
			,c.[Pet_Name]
			,a.姓名
	INTO #user_cathealth     
	FROM [Pet].[dbo].[貓咪狀況記錄] c inner join  [dbo].[會員] a on c.user_ID = a.user_ID;

	select * from #user_cathealth uc inner join [dbo].[過敏原] aa on uc.Pet_ID = aa.Pet_ID 
END
go


exec create_user_catcondition_allergic_agent ; 


