use Pet
go

CREATE OR ALTER PROCEDURE create_user_catcondition
AS BEGIN
	-- �]���ϥΪ̿�J�A���|��J�����ID  �ϥΪ̩m�W  �������ߦW �����ǹL�ӭ� 
	--�|�� ���p �߫}���p�O�� ���p �L�ӭ��\
	--��K �d�� �߫}ID & �̷s������� & �L�ӭ� �O ������?????
    SELECT	a.[user_ID]
			,c.[Pet_ID]
			,c.[Pet_Name]
			,a.�m�W
			      ,[�������]
      ,[��ĥͤ�]
      ,[�ʧO]
      ,[�魫]
      ,[���q]
      ,[�ܤ��q]
      ,[�p�K����]
      ,[�K�K�ƶq]
      ,[�ɱ`���o]
      ,[�y���\]
      ,[�Ե}]
      ,[�æR]
      ,[�W��]
	INTO #user_cathealth_     
	FROM [Pet].[dbo].[�߫}���p�O��] c   join  [dbo].[�|��] a on c.user_ID = a.user_ID

	SELECT  * from #user_cathealth_;   
END
go

use Pet
exec create_user_catcondition;
