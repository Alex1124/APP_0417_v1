USE Pet
GO

-- �n�J
CREATE OR ALTER PROCEDURE LOGIN
    @fullname NVARCHAR(15),
    @account NVARCHAR(15),
    @password NVARCHAR(15),
    @email NVARCHAR(max)
AS
BEGIN
    BEGIN TRY
        IF EXISTS (SELECT * FROM [dbo].[�|��] WHERE [�m�W] = @fullname AND [�b��] = @account AND [�K�X] = @password AND [�H�c] = @email)
        SELECT A.user_ID, B.Pet_ID FROM [dbo].[�|��] A INNER JOIN [dbo].[�߫}���p�O��] B
            ON A.[user_ID] = B.[user_ID]
            WHERE A.[�m�W] = @fullname AND A.[�b��] = @account AND A.[�K�X] = @password AND A.[�H�c] = @email
        ELSE SELECT 'NO REGISTER' AS [MESSAGE];
    END TRY
    BEGIN CATCH
        SELECT ERROR_MESSAGE() AS [MESSAGE];
    END CATCH;
END
GO


-- �إߨ��
CREATE OR ALTER FUNCTION dbo.sidautoadd ()
RETURNS nvarchar(50)
AS
BEGIN
    DECLARE @result nvarchar(50);
    DECLARE @new_id int = COALESCE((SELECT MAX(CAST(SUBSTRING(user_ID, 3, 5) AS int)) FROM [dbo].[�|��]), 0) + 1;
    SET @result = 'AF' + RIGHT('0' + CAST(@new_id AS nvarchar(5)), 5);
    RETURN @result;
END
GO

-- ���U
CREATE OR ALTER PROCEDURE REGISTER
@fullname NVARCHAR(15),
@account NVARCHAR(15),
@password NVARCHAR(15),
@email NVARCHAR(max)
AS
        BEGIN
            BEGIN TRY
            DECLARE @new_id nvarchar(50) = dbo.sidautoadd();
            IF (SELECT COUNT(*) FROM [dbo].[�|��] WHERE [�H�c] = @email) > 0
                SELECT 'registered' AS [MESSAGE]
            ELSE
                BEGIN
                    INSERT INTO [dbo].[�|��] ([user_ID], [�m�W], [�b��], [�K�X], [�H�c]) 
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

select * from [dbo].[�|��]