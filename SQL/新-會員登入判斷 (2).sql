USE Pet
GO

-- 登入
CREATE OR ALTER PROCEDURE LOGIN
    @fullname NVARCHAR(15),
    @account NVARCHAR(15),
    @password NVARCHAR(15),
    @email NVARCHAR(max)
AS
BEGIN
    BEGIN TRY
        IF EXISTS (SELECT * FROM [dbo].[會員] WHERE [姓名] = @fullname AND [帳號] = @account AND [密碼] = @password AND [信箱] = @email)
        SELECT A.user_ID, B.Pet_ID FROM [dbo].[會員] A INNER JOIN [dbo].[貓咪狀況記錄] B
            ON A.[user_ID] = B.[user_ID]
            WHERE A.[姓名] = @fullname AND A.[帳號] = @account AND A.[密碼] = @password AND A.[信箱] = @email
        ELSE SELECT 'NO REGISTER' AS [MESSAGE];
    END TRY
    BEGIN CATCH
        SELECT ERROR_MESSAGE() AS [MESSAGE];
    END CATCH;
END
GO


-- 建立函數
CREATE OR ALTER FUNCTION dbo.sidautoadd ()
RETURNS nvarchar(50)
AS
BEGIN
    DECLARE @result nvarchar(50);
    DECLARE @new_id int = COALESCE((SELECT MAX(CAST(SUBSTRING(user_ID, 3, 5) AS int)) FROM [dbo].[會員]), 0) + 1;
    SET @result = 'AF' + RIGHT('0' + CAST(@new_id AS nvarchar(5)), 5);
    RETURN @result;
END
GO

-- 註冊
CREATE OR ALTER PROCEDURE REGISTER
@fullname NVARCHAR(15),
@account NVARCHAR(15),
@password NVARCHAR(15),
@email NVARCHAR(max)
AS
        BEGIN
            BEGIN TRY
            DECLARE @new_id nvarchar(50) = dbo.sidautoadd();
            IF (SELECT COUNT(*) FROM [dbo].[會員] WHERE [信箱] = @email) > 0
                SELECT 'registered' AS [MESSAGE]
            ELSE
                BEGIN
                    INSERT INTO [dbo].[會員] ([user_ID], [姓名], [帳號], [密碼], [信箱]) 
                    VALUES (@new_id, @fullname, @account, @password, @email)
                    SELECT 'registration success' AS [MESSAGE]
                END
        END TRY
    BEGIN CATCH
        SELECT ERROR_MESSAGE() AS [MESSAGE];
    END CATCH;
END
GO


EXEC REGISTER @fullname='9999', @account='nds741852', @password='741822', @email='e99999666@gmail.com'
GO

select * from [dbo].[會員]