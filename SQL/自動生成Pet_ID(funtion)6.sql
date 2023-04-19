CREATE OR ALTER FUNCTION dbo.autopet ()
RETURNS nvarchar(5)
AS
BEGIN
    DECLARE @result nvarchar(5);
    DECLARE @new_id int = COALESCE((SELECT MAX(CAST(SUBSTRING(Pet_ID, 3, 5) AS int)) FROM [dbo].[�߫}���p�O��]), 0) + 1;
    SET @result = 'CK' + RIGHT(CAST(@new_id AS nvarchar(3)), 3);
    RETURN @result;
END
GO


--����
--select dbo.autopet ()