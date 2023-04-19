use Pet
go

CREATE OR ALTER PROCEDURE createproduct
AS BEGIN
    SELECT A.產品代碼,E.品牌名稱,A.產品名稱,A.商品種類,A.適用年齡,A.圖片,C.價格,D.賣家名稱 
    INTO ##product_price
    FROM [dbo].[產品] A,[dbo].[價格表] C,賣家 D,品牌 E
    WHERE A.產品代碼 = C.產品代碼  AND C.賣家代號 = D.賣家代號 AND A.品牌代號 = E.品牌代號
    ORDER BY A.產品代碼
    SELECT * FROM ##product_price
END
go

exec createproduct;




