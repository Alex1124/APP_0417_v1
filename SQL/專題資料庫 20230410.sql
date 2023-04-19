--CREATE DATABASE Pet
USE Pet

CREATE TABLE ��a (
                ��a�N�� NVARCHAR(2) NOT NULL,
                ��a�W�� NVARCHAR(15) NOT NULL,
                  PRIMARY KEY (��a�N��)
)

CREATE TABLE �~�P (
                �~�P�N�� NVARCHAR(5) NOT NULL,
                �~�P�W�� NVARCHAR(20) NOT NULL,
                  PRIMARY KEY (�~�P�N��)
)


CREATE TABLE �q�� (
                �~�P�N�� NVARCHAR(5) NOT NULL,
                ��a�N�� NVARCHAR(2) NOT NULL,
                  PRIMARY KEY (�~�P�N��, ��a�N��)
)




CREATE TABLE ���~ (
                ���~�N�X NVARCHAR(6) NOT NULL,
                �~�P�N�� NVARCHAR(5) NOT NULL,
                ���~�W�� NVARCHAR(MAX) NOT NULL,
                �ӫ~���� NVARCHAR(4) NOT NULL,
                �A�Φ~�� NVARCHAR(3) NOT NULL,
                �Ϥ� NVARCHAR(50) NOT NULL,
                  PRIMARY KEY (���~�N�X)
)

CREATE TABLE ���� (
                ���~�N�X NVARCHAR(6) NOT NULL,
                ����1 NVARCHAR(50),
                ����2 NVARCHAR(50),
                ����3 NVARCHAR(50),
                ����4 NVARCHAR(50),
                ����5 NVARCHAR(50),
                ����6 NVARCHAR(50),
                ����7 NVARCHAR(50),
                ����8 NVARCHAR(50),
                ����9 NVARCHAR(50),
                ����10 NVARCHAR(50),
                ����11 NVARCHAR(50),
                ����12 NVARCHAR(50),
                ����13 NVARCHAR(50),
                ����14 NVARCHAR(50),
                ����15 NVARCHAR(50),
                  PRIMARY KEY (���~�N�X)
)

CREATE TABLE �|�� (
                user_ID NVARCHAR(5) NOT NULL,
                �m�W NVARCHAR(15) NOT NULL,
                �b�� NVARCHAR(15) NOT NULL,
                �K�X NVARCHAR(15) NOT NULL,
                �H�c NVARCHAR(MAX) NOT NULL,
                  PRIMARY KEY (user_ID)
)

CREATE TABLE �߫}���p�O�� (
                user_ID NVARCHAR(5) NOT NULL,
                Pet_ID NVARCHAR(5) NOT NULL,
                Pet_Name NVARCHAR(30) NOT NULL,
                ������� DATE NOT NULL ,
                ��ĥͤ� DATE NOT NULL,
                �ʧO NVARCHAR(2) NOT NULL,
                �魫 DECIMAL(6,2),
                ���q TINYINT,
                �ܤ��q TINYINT,
                �p�K���� TINYINT,
                �K�K�ƶq TINYINT,
                �ɱ`���o TINYINT,
                �y���\ TINYINT,
                �Ե} TINYINT,
                �æR TINYINT,
                �W�� TINYINT,
                PRIMARY KEY (Pet_ID,�������)
)

CREATE TABLE �L�ӭ� (
                Pet_ID NVARCHAR(5) NOT NULL,
                ������� DATE NOT NULL,
                �L�ӭ�1 NVARCHAR(7),
                �L�ӭ�2 NVARCHAR(7),
                �L�ӭ�3 NVARCHAR(7),
                �L�ӭ�4 NVARCHAR(7),
                �L�ӭ�5 NVARCHAR(7),
                �L�ӭ�6 NVARCHAR(7),
                �L�ӭ�7 NVARCHAR(7),
                �L�ӭ�8 NVARCHAR(7),
                �L�ӭ�9 NVARCHAR(7),
                �L�ӭ�10 VARCHAR(7),
                PRIMARY KEY (Pet_ID,�������)
)

CREATE TABLE �����(
                    ��a�N�� NVARCHAR(2) NOT NULL,
                    ���~�N�X NVARCHAR(6) NOT NULL,
                    ���� INT NOT NULL,
                    PRIMARY KEY(��a�N��,���~�N�X)
                   )


ALTER TABLE �q�� ADD  
FOREIGN KEY (��a�N��)
REFERENCES ��a (��a�N��)
ON DELETE NO ACTION
ON UPDATE NO ACTION


ALTER TABLE �q�� ADD  
FOREIGN KEY (�~�P�N��)
REFERENCES �~�P (�~�P�N��)
ON DELETE NO ACTION
ON UPDATE NO ACTION



ALTER TABLE ���~ ADD  
FOREIGN KEY (�~�P�N��)
REFERENCES �~�P (�~�P�N��)
ON DELETE NO ACTION
ON UPDATE NO ACTION



ALTER TABLE ���� ADD  
FOREIGN KEY (���~�N�X)
REFERENCES ���~ (���~�N�X)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE �߫}���p�O�� ADD  
FOREIGN KEY (user_ID)
REFERENCES �|�� (user_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE �L�ӭ� ADD  
FOREIGN KEY (Pet_ID,�������)
REFERENCES �߫}���p�O�� (Pet_ID,�������)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE ����� ADD
FOREIGN KEY (��a�N��)
REFERENCES ��a (��a�N��)

ALTER TABLE ����� ADD
FOREIGN KEY (���~�N�X)
REFERENCES ���~ (���~�N�X)