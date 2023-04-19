import numpy as np
import pandas as pd
from datetime import datetime, date
from collections import OrderedDict
from pathlib import Path
from collections import OrderedDict


from flask import Flask, redirect, url_for ,request, render_template, Blueprint , jsonify, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy

# 日期 錯誤 順序 第一個 大 第二個小 錯
#  IndexError: single positional indexer is out-of-bounds

 
## 載入自訂義function 函式or class 類別

from view.load_db import load_files
from view.my_log import my_logging
# from load_db import load_files, get_user_select_allergic_of_the_cat

#註冊blueprint 讓flask 定義的app 路由位址(網址) 在app.py註冊後，經由main.py執行可以使用有註冊過的/網址
recommend_page = Blueprint('recommend_page', __name__)
dev_logger = my_logging()





def Cat_health_care_table_to_helpful():
    """### 貓咪狀況轉換成貓咪有幫助成分 ex 拉西 = > 乳酸桿菌 字典
    df_cat_health_care : dataframe, 貓咪狀況表
    keys 索引, values 值"""

    dict_CHC2REC= OrderedDict()
    keys = [ '頻尿', '拉稀', '嘔吐', '流眼淚', '便便數量', '小便次數', '飯量', '喝水量', '老齡貓', '幼貓', '肥胖' ,  '時常抓癢'   ] 

    values = [ ['水', '蔓越莓', '葡萄糖胺','綠唇貽貝', '離胺酸(Lysine)', '色胺酸', 'GABA', '綠茶'], #頻尿
              ['乳酸桿菌L.acidophilus', '雙歧桿菌Bifidobacterium animalis', '鼠李糖乳桿菌L.rhamnosus(LGG)', '發酵乳酸桿菌L.fermentum', '益生菌', '南瓜', '色胺酸', '綠唇貽貝'],  ## 拉稀1
                 ['南瓜', '益生菌', '酵素', '洋車前子', '水解胜肽蛋白'],    #嘔吐
                 [ '離胺酸(Lysine)', '葉黃素(Lutein)', '牛磺酸', '葡聚醣', ['玉米', '小麥', '大豆'] ], ## 流眼淚 排除 玉米 小麥 大豆['玉米', '小麥', '大豆']
                  ['水', '益生菌', '維生素E', '蔬菜', '纖維', '洋車鉗子', '南瓜', '貓草', '小麥草', '地瓜', '酵素', '油'],   #便便數量
                  ['水'],  #小便次數
              ['魚', '雞肉', '雞肉絲', '鮭魚', '火雞肉', '鴨肉', '羊肉', '牛肉', '鵪鶉', '鮪魚', '蝦', '土雞肉', '雞蛋黃', '雞腿', '鹿肉', '袋鼠肉' , '益生菌', '水解胜肽蛋白'],#飯量 魚(可按照位置改變分數)
               ['水'], #喝水量1
                 [ '雞肉', '雞肉絲', '鮭魚', '火雞肉', '鴨肉', '羊肉', '牛肉', '鵪鶉', '鮪魚', '蝦', '土雞肉', '雞蛋黃', '雞腿', '鹿肉', '袋鼠肉',
                  '水解胜肽蛋白', '牛磺酸', '雞胸', '離胺酸', '脂肪酸', '維他命'],  ##老齡貓
                 ['雞肉', '雞肉絲', '鮭魚', '火雞肉', '鴨肉', '羊肉', '牛肉', '鵪鶉', '鮪魚', '蝦', '土雞肉', '雞蛋黃', '雞腿', '鹿肉', '袋鼠肉', '離胺酸', '鈣', '牛磺酸' ], #幼貓
                 ['雞肉', '雞肉絲', '鮭魚', '火雞肉', '鴨肉', '羊肉', '牛肉', '鵪鶉', '鮪魚', '蝦', '土雞肉', '雞蛋黃', '雞腿', '鹿肉', '袋鼠肉', '膳食纖維', '綠唇貽' ], #肥胖
                 [] #心理壓力大 maybe to do
                 
                 ]  

    for key, value in zip(keys, values):
            dict_CHC2REC[key] = value

    # print(f"貓咪健康照顧狀況>>推薦成分 字典: {dict_CHC2REC}\n")

    return dict_CHC2REC

def age(born:datetime):
    "生日轉換成年齡"
    born = datetime.strptime(born, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month,  born.day))


def get_user_select_allergic_of_the_cat(username:str, cat_name:str, start:str, end:str, df_allergic:pd.DataFrame):
    """### df_allergic 過敏原 X 貓咪 X 主人表，取得使用者篩選的 過敏原串列
    Index(['user_ID', 'Pet_ID', 'Pet_Name', '姓名', 'Pet_ID', '紀錄日期', 
    '過敏原1', '過敏原2','過敏原3', '過敏原4', '過敏原5', '過敏原6', '過敏原7', '過敏原8', '過敏原9', '過敏原10'], dtype='object')"""

    # print("過敏原綜合表欄位: \n\n", df_allergic.keys()) 

    #文字轉換成日期格式
    # df_allergic['紀錄日期'] = pd.to_datetime(df_allergic['紀錄日期'], unit='True')  
    start, end = datetime.strptime(start, '%Y-%m-%d').date(), datetime.strptime(end, '%Y-%m-%d').date()

    # 測試日期
    # username = "海雯綺"
    # cat_name = "Tristian" ## Abbas Sydnee Aegle Tristian Dane Melany
    # start , end = '2020-10-10', '2023-01-19'
    
    # 建立篩選條件遮罩 日期範圍 貓名 使用者名稱

    date_range_mask = ( df_allergic['紀錄日期'] >= start ) & ( df_allergic['紀錄日期'] <= end )
    cat_name_mask = ( df_allergic['Pet_Name'] == cat_name )
    username_mask = ( df_allergic['姓名'] == username )

    # 篩選條件後的 df_filted
    df_filted = \
    df_allergic[ date_range_mask & cat_name_mask & username_mask ].sort_values(by='紀錄日期', axis=0, ascending=True).iloc[:, 6:]
    # 去除重複的過敏原 時間範圍內
    df_filted = df_filted.drop_duplicates([ '過敏原1', '過敏原2','過敏原3', '過敏原4', '過敏原5', '過敏原6', '過敏原7', '過敏原8', '過敏原9', '過敏原10'], keep='first') 
    temp = set()
    for i in  range(df_filted.shape[0]):
        for value in df_filted.values[i]:
            # print(value)
            if value != 'nan' and  value  != '':
                temp.add(value)
    
    df_filted = list(temp)

    return df_filted

def cat_health_care_daterange(username:str, cat_name:str, start:str, end:str, df_cat_health:pd.DataFrame, df_allergic:pd.DataFrame):
    """### 建立使用者選取的日期範圍的貓咪健康狀態 平均或比率, 與輸出 篩選後的過敏原list
    ### catname 貓名, start 開始日期 end 結束日期 df_cat_health 貓咪健康狀況記錄表 df_allergic 過敏原總表"""
    
    #取得 使用者 and 特定貓 and start 天 紀錄~ end 天 之間的 最新的過敏原紀錄
    allergic_list : list = get_user_select_allergic_of_the_cat(username, cat_name, start, end, df_allergic) 
    
    # df = pd.read_csv(Path('SQL\貓咪狀況紀錄.csv'))
    df = df_cat_health 
    # print(df.keys())
    
    #文字轉換成日期格式
    # df['紀錄日期'] = pd.to_datetime(df['紀錄日期']) 
    start, end = datetime.strptime(start, '%Y-%m-%d').date(), datetime.strptime(end, '%Y-%m-%d').date()
    
    # 測試日期
    # username = "海雯綺"
    # cat_name = "Tristian" ## Abbas Sydnee Aegle Tristian Dane Melany
    # start , end = '2020-10-10', '2023-01-19'
    # 建立篩選條件遮罩 日期範圍 貓名 使用者名稱
    date_range_mask = ( df['紀錄日期'] >= start ) & ( df['紀錄日期'] <= end )
    cat_name_mask = ( df['Pet_Name'] == cat_name )
    username_mask = ( df['姓名'] == username )   ####

    # 篩選條件後的 df_filted
    # print("檢查 過濾前 的df: ",df )
    df_filted = df[ date_range_mask & cat_name_mask & username_mask ]
    # print("檢查 過濾後 的df: ",df_filted )
    # 設定貓咪狀況字典
    mean_rate_cat_condiction_dict = OrderedDict()
 
 
    for col in df_filted[['飯量', '喝水量', '流眼淚', '拉稀', '嘔吐', '時常抓癢','頻尿']].columns :
        # print( df[ date_range_mask & cat_name_mask ][[col]].value_counts())
        # 確認布林值 他的數值分布是否 0 和 1 如果是 則 形狀大小> 1
        if df_filted[[col]].value_counts().values.shape[0] > 1 :
            # print(col)
            mean_rate_cat_condiction_dict[col] = df_filted[[col]].value_counts()[ df_filted[[col]].value_counts().values == df_filted[[col]].value_counts().values.max() ].index[0][0]  #取得飯量 0 和 1狀態之間最多的 是誰?

        # 確認布林值 他的數值分布是否 0 或 1 如果是 則 形狀大小== 1
        if df_filted[[col]].value_counts().values.shape[0] == 1 :
            mean_rate_cat_condiction_dict[col] = df_filted[[col]].value_counts()[ df_filted[[col]].value_counts().values == df_filted[[col]].value_counts().values.max() ].index[0][0]  #取得飯量 0 或 1狀態之間最多的 是誰?

    #新增 連續數值欄位，平均後儲存到字典
    keys = ['體重', '小便次數', '便便數量']
    values = df_filted[['體重', '小便次數', '便便數量']].mean()
    for key, value in zip(keys, values):
        mean_rate_cat_condiction_dict[key] = round( value, 2 )

    # 新增其他重要資訊到字典
    keys = ['姓名', 'Pet_ID', 'Pet_Name', '毛孩生日', '紀錄日期']
    # print(df_filted)
    # print(df_filted[['Pet_ID', 'Pet_Name', '毛孩生日']].values.tolist())
    values = df_filted[['姓名', 'Pet_ID', 'Pet_Name', '毛孩生日', '紀錄日期']].values.tolist()[0]
    # print(values)
    for key, value in zip(keys, values):
        mean_rate_cat_condiction_dict[key] = value

    ## 建立使用者選取的日期範圍的健康狀態 DF
    mean_rate_cat_condiction_df = pd.DataFrame(dict(mean_rate_cat_condiction_dict), index=[0])

    # 輸出貓咪平均狀況df 使用者搜尋特定貓咪特定日期範圍的df_allergic_list
    return mean_rate_cat_condiction_df, allergic_list

def select_cat_to_recommend_ingredients(df_product:pd.DataFrame, mean_rate_cat_condiction_df:pd.DataFrame, cat_name:str, dict_CHC2REC:dict):  
    """### 選擇某隻貓咪，根據狀況推薦，輸出 推薦成分, 有害成分-->list, 產品表, 貓咪狀況_已篩選過 -->dataframe 
    df_product : 產品表
    mean_rate_cat_condiction_df : dataframe, 使用者姓名 貓名 日期範圍 篩選條件後 的 貓咪狀況
    cat_name : string, 查詢哪隻貓咪
    dict_CHC2REC : dict, 貓咪狀況轉換成貓咪有幫助成分 ex 拉西 = > 乳酸桿菌"""

    df_cat_health = mean_rate_cat_condiction_df
    
    # 轉換生日為年齡
    df_cat_health['毛孩生日']= df_cat_health['毛孩生日'].astype(str).apply(age) 
    df_cat_health.rename( columns={'毛孩生日' : '年齡'},  inplace=True)
    
    dev_logger.info(f"{cat_name}貓咪健康平均比率狀況: \n{df_cat_health}")
    
    # 貓咪推薦 或 有害篩除成份
    Cat_recommend = []
    Cat_harmful = []

    # 貓咪狀況條件判斷
    if ( df_cat_health['頻尿'].values[0] > 0 )  :
            Cat_recommend.extend( dict_CHC2REC['頻尿'])

    if ( df_cat_health['拉稀'].values[0] > 0 ) :
            Cat_recommend.extend( dict_CHC2REC['拉稀'])

    if ( df_cat_health['嘔吐'].values[0] > 0 )  :
            Cat_recommend.extend( dict_CHC2REC['嘔吐'])

    if ( df_cat_health['流眼淚'].values[0] > 0 ) :
            Cat_recommend.extend( dict_CHC2REC['流眼淚'])
            Cat_harmful.extend(dict_CHC2REC['流眼淚'][-1])  #有害

    if  ( df_cat_health['飯量'].values[0] > 0 )  :
            Cat_recommend.extend( dict_CHC2REC['飯量'])

    if ( df_cat_health['喝水量'].values[0] > 0 ) :
            Cat_recommend.extend( dict_CHC2REC['喝水量'])
    

    if df_cat_health['便便數量'].values[0] <= 2 :
            Cat_recommend.extend( dict_CHC2REC['便便數量'])
            
    if  (df_cat_health['小便次數'].values[0] <= 1) | (df_cat_health['小便次數'].values[0] >= 7)  :
            Cat_recommend.extend( dict_CHC2REC['小便次數'])
    
    if  (df_cat_health['年齡'].values[0] > 7 )  :
            Cat_recommend.extend( dict_CHC2REC['老齡貓'])
    
    if  (df_cat_health['年齡'].values[0] <= 1 )  :
            Cat_recommend.extend( dict_CHC2REC['幼貓'])

    #判斷是否 幼貓肥胖 成貓肥胖
    if ( (df_cat_health['年齡'].values[0] <= 1 ) &  (df_cat_health['體重'].values[0] > 4) ) | ( ( df_cat_health['年齡'].values[0] > 1 ) &  (df_cat_health['體重'].values[0] > 6 ) ) : #肥胖 幼貓 成貓
            Cat_recommend.extend( dict_CHC2REC['肥胖'])
            ## 如果肥胖 要排除商品種類 貓咪飼料
            dev_logger.info(f"這隻 {cat_name}貓 肥胖 \n排除商品種類: 貓咪飼料")
            
            # #### 排除產品表 的 貓咪飼料種類 ####
            df_product = df_product[ df_product['商品種類'] != '貓咪飼料' ]

    ## 排除重複成分
    Cat_recommend, Cat_harmful = list(set(Cat_recommend)), list(set(Cat_harmful))        
    
    dev_logger.info(f"這隻 {cat_name}貓 推薦成分:\n{Cat_recommend}")  
    dev_logger.info(f"這隻 {cat_name}貓 排除成分:\n{Cat_harmful}")
    
    return Cat_recommend, Cat_harmful, df_product, df_cat_health



def Max_Min(df:pd.DataFrame):
    "### 資料正規化，得到數值區間[0,1]"

    normalization =(df - df.min() ) / ( df.max() - df.min() )
    # print(f"{normalization[:5]}")
    return normalization



def Cat_helpful_scores(df_cat_health:pd.DataFrame, df_ingredient:pd.DataFrame, cat_recommend_ingredients:list,
                       cat_harmful:list, cat_allergic_agent_list:list, mode:bool=False):
    """將特定貓咪健康狀況，得到特定推薦成分與該貓咪要避免的過敏原當輸入，檢索 產品成分表，得到有幫助分數 與有害分數，
        相加後 Max_Min 正規化 + 偏差[ 隨機亂數(極小方便使用者沒輸入也能排序推薦) ] 
        ### >> 輸出產品成分評分表
        
        df_cat_health : df, 條件篩選與平均比率後的貓咪狀況
        df_ingredient : df, 成分表, 讀取後有轉置
        cat_recommend_ingredients : list, 貓咪推薦成分
        cat_harmful : list,貓咪排除成分
        cat_allergic_agent_list : list, 過敏原成分表轉串列
        mode : string, True : 隨機賦予分數, False : 按照貓咪狀況評分
        
    """
    # 轉置 
    df_ingredient = df_ingredient.T 

    # 設定初始值
    scores_help = df_ingredient.iloc[1:, :].isin( []).sum(axis=0)
    
    # 如果沒隨機推薦
    if mode == False:
        # 普通計算 單純確認成分有無在裡面
        # 檢查是有無推薦成分
        scores_help = df_ingredient.iloc[1:, :].isin( cat_recommend_ingredients).sum(axis=0)

        # 順序 
        # 特殊計算
        # 成分1 =  要有水
        if ( df_cat_health['頻尿'].values[0] > 0 )  | ( df_cat_health['便便數量'].values[0] <= 2 ) | (df_cat_health['小便次數'].values[0] <= 1) | (df_cat_health['小便次數'].values[0] >= 7) | ( df_cat_health['喝水量'].values[0] > 0 ):
            scores_help.iloc[df_ingredient.loc[:, df_ingredient.iloc[1,:].str.contains('水', case=True) ].head().columns ] = scores_help.iloc[df_ingredient.loc[:, df_ingredient.iloc[1,:].str.contains('水', case=True) ].head().columns ] + 1

        # 魚 按順序 有不同分數
        if  ( df_cat_health['飯量'].values[0] > 0 ) :
            scores_help.iloc[df_ingredient.loc[:, df_ingredient.iloc[1,:].str.contains('魚', case=True) ].head().columns ] = scores_help.iloc[df_ingredient.loc[:, df_ingredient.iloc[1, :].str.contains('魚', case=True) ].head().columns ] + 1
            scores_help.iloc[df_ingredient.T[ df_ingredient.T['成分2'].str.contains('魚') == True ].T.head().columns ] = scores_help.iloc[df_ingredient.T[ df_ingredient.T['成分2'].str.contains('魚') == True ].T.head().columns ] + 0.5
            scores_help.iloc[df_ingredient.T[ df_ingredient.T['成分3'].str.contains('魚') == True ].T.head().columns ] = scores_help.iloc[df_ingredient.T[ df_ingredient.T['成分3'].str.contains('魚') == True ].T.head().columns ] + 0.25   

        # 雞肉 按順序 有不同分數

        if  ( df_cat_health['飯量'].values[0] > 0 ) | (df_cat_health['年齡'].values[0] > 7 ) | (df_cat_health['年齡'].values[0] <= 1 ) | \
        ( (df_cat_health['年齡'].values[0] <= 1 ) &  (df_cat_health['體重'].values[0] > 4) ) | ( ( df_cat_health['年齡'].values[0] > 1 ) &  (df_cat_health['體重'].values[0] > 6 ) ) :
            
            scores_help.iloc[df_ingredient.loc[:, df_ingredient.iloc[1,:].str.contains('雞肉', case=True) ].head().columns ] = scores_help.iloc[df_ingredient.loc[:, df_ingredient.iloc[1, :].str.contains('雞肉', case=True) ].head().columns ] + 1
            scores_help.iloc[df_ingredient.T[ df_ingredient.T['成分2'].str.contains('雞肉') == True ].T.head().columns ] = scores_help.iloc[df_ingredient.T[ df_ingredient.T['成分2'].str.contains('雞肉') == True ].T.head().columns ] + 0.5
            scores_help.iloc[df_ingredient.T[ df_ingredient.T['成分3'].str.contains('雞肉') == True ].T.head().columns ] = scores_help.iloc[df_ingredient.T[ df_ingredient.T['成分3'].str.contains('雞肉') == True ].T.head().columns ] + 0.25

        # 有害排除成分 
        scores_harm = df_ingredient.iloc[1:, :].isin( cat_harmful).sum(axis=0)
        scores_allergic = df_ingredient.iloc[1:, :].isin( cat_allergic_agent_list).sum(axis=0)
        
        # 依據貓咪推薦成分得到的產品表商品有幫助分數 減掉 依據貓咪過敏原所得到的商品有害分數 = 貓咪加權分數
        scores_help -= ( scores_harm + scores_allergic )
        
        dev_logger.info(f"分數分布: \n{scores_help.value_counts()}")
    else:
        # 隨機推薦將推薦分數設為0
        scores_help[:] = 0

    # 貓咪加權分數 Max_Min + 偏差(極小小數隨機亂數)
    Product_Rating = Max_Min(scores_help) + (np.random.random(size= scores_help.shape) / 10)
    
    # 合併成分表與評分 ==>> 得到成分評分表
    Product_Rating_table =pd.concat([df_ingredient.T, Product_Rating], axis=1)
    Product_Rating_table = Product_Rating_table.rename(columns={0 : '評分'})    
    Product_Rating_table.sort_values(by='評分', ascending=False, inplace=True)
    # print(Product_Rating_table.head()[['產品代碼', '評分']])

    # 轉換 輸出產品成分評分表 什麼產品(產品代碼) 有什麼評分
    Product_Rating_table = Product_Rating_table[['產品代碼', '評分']]
    # dev_logger.info(f"final Product_Rating_table: {Product_Rating_table.head()} \n")
    
    return Product_Rating_table


def Recommend( Product_Rating_table:pd.DataFrame, merge_product:pd.DataFrame, sort_key='評分',therehold=0.2, recommend_num=8 , *arg, **args):
    """#### 商品評分表Product_Rating_table sorted(商品評分) 檢索前therehold ,隨機取 recommend_num 個 的Index 查詢 merge_product 推薦商品
        merge_product : 產品表 合併 成分表 
    """
    
    # 合併總表 產品 成分 評分
    # 主鍵 '產品代碼' 取 交集
    Product_Rating_table_all = pd.merge(Product_Rating_table, merge_product, on='產品代碼', how='inner', sort=True)
    # Product_Rating_table_all.to_csv('Product_Rating_table_all.csv')
    # print('產品表合併產品成分評分表:', Product_Rating_table_all)

    # 排序
    Product_Rating_table_all = Product_Rating_table_all.sort_values(by=[sort_key], ascending=False, axis=0)

    # 商品總數
    total_product_num = Product_Rating_table_all.shape[0]
    dev_logger.info(f"商品數量 {total_product_num}")

    # 依靠闕值 計算 商品數量20% 數量
    product_20_num = int(total_product_num * therehold)
    dev_logger.info(f"商品數量20% = {product_20_num}")

    # 商品數量前20% 隨機取 推薦數 Recommend_num 的 index
    recommend_num = 8

    # 取得推薦商品的index recommend_num = 8 個
    Recommend_product_index_list = np.random.choice(a= np.arange(0, product_20_num ), size=(recommend_num, ), replace=False).tolist()

    # 推薦 推薦數 個商品
    Product_Rating_table_filterd = Product_Rating_table_all.iloc[Recommend_product_index_list, ]

    # 關聯 商品總表 取得 所需欄位訊息 產品代碼 商品標題 圖片名稱 價格 評分 商品種類 網頁連結
    Product_Rating_table_filterd = Product_Rating_table_filterd.iloc[:, : ].sort_values(by=[sort_key], ascending=False, axis=0)
    Product_Rating_table_filterd.to_csv(Path('log') / "Product_Rating_table_filterd.csv")
    dev_logger.info(f"推薦表: \n{Product_Rating_table_filterd}")
    
    return Product_Rating_table_filterd 



# 貓咪健康狀況查詢 與推薦 /health
# 日期查詢超出範圍 IndexError: single positional indexer is out-of-bounds

@recommend_page.route('/query',  methods=['GET', 'POST'])
def query():

    print(f"現在app有哪些{session.keys()}") 
    for key in session.keys():
        print(session[key], end='\t')
    
    # 取得 登入後session 存資料庫該會員的資料
    # master = session.get('fullname') 誰?
    # cats 有幾隻貓?貓名? 那麼 提示使用者輸入那幾隻貓名，如果不是那些貓名請重新輸入

    
    try:
        # 如果有登入，則執行以下區塊
        assert session['logged_in'] == True
    except Exception as e:
        dev_logger.error(f"Catch an exception. - {e}", exc_info=True)
        # 沒登入跳轉到登入
        return redirect(url_for('login_page.signup'))

    try:
        if request.method == 'POST':
            
            #取得使用者 貓咪名稱 日期範圍
            """雪蓮婷 海雯綺 劉俐彤"""
            catname = request.values['petname']   #透過HTML 屬性 取得 使用者輸入貓名 petname
            startdate = request.values['start_date']   #透過HTML 屬性 取得 使用者輸入貓名 start_date
            enddate = request.values['end_date']            #透過HTML 屬性 取得 使用者輸入end_date
            master = session.get('fullname')
            
            _, _, df, _ = load_files()
            # if df[df['Pet_Name'] == catname ]['姓名'].unique().shape[0] < 2:
            #     master =  df[df['Pet_Name'] == catname ]['姓名'].unique()[0]      
            # cat_name = "Tristian" ## Abbas Sydnee Aegle Tristian Dane Melany
            # start , end = '2020-10-10', '2023-01-19'
            
            # 轉換日期格式，找到資料庫中 符合資料的日期 開始~結束
            
            try:
                startdate, enddate = datetime.strptime(startdate, '%Y-%m-%d').date(), datetime.strptime(enddate, '%Y-%m-%d').date()
                if startdate > enddate :
                    startdate, enddate =  enddate, startdate

            except Exception as e:
                dev_logger.error(f"使用者輸入日期錯誤 - {e}", exc_info=True)
                return redirect(url_for('recommend_page.query'))
            
            date_range_mask = ( df['紀錄日期'] >= startdate ) & ( df['紀錄日期'] <= enddate )
            cat_name_mask = ( df['Pet_Name'] == catname )
            user_name_mask = ( df['姓名'] == master )
            df_filted = df[ date_range_mask & cat_name_mask & user_name_mask ].sort_values(by='紀錄日期', ascending=True)
            try:
                startdate, enddate = df_filted['紀錄日期'].iloc[0] , df_filted['紀錄日期'].iloc[-1]

            except Exception as e:
                dev_logger.error(f"資料比數錯誤 - {e}", exc_info=True)
                return redirect(url_for('recommend_page.query'))
            dev_logger.info(f"{master}, {catname}, {startdate} , {enddate}" )


            return render_template('inquire.html', **locals())


        return render_template('inquire_no_diagram.html')

    except Exception as e:
        dev_logger.error(f"Catch an exception. - {e}", exc_info=True)

        return render_template('inquire_no_diagram.html')

# 貓咪健康狀況查詢 與推薦 /health
@recommend_page.route('/recommend',  methods=['GET', 'POST'])
def recommend():

    try:
        # 如果有登入，則執行以下區塊
        assert session['logged_in'] == True
    except Exception as e:
        dev_logger.error(f"Catch an exception. - {e}", exc_info=True)
        # 沒登入跳轉到登入
        return redirect(url_for('login_page.signup'))
    
    try:

        #取得資料庫資料回傳 產品表 成分表 貓咪健康狀況表 過敏原總表#
        df_pro, df_ingre, df_cath, df_allergic  = load_files()
        # #### 產品與成分合併 總表 ####
        merge_product = pd.merge(df_pro, df_ingre, on='產品代碼', how='inner', sort=True)
        #根據貓咪健康狀況，設計轉換成推薦成份的字典 
        dict_CHC2REC = Cat_health_care_table_to_helpful() 

        username = request.args.get('username')
        cat_name = request.args.get('cat_name')
        start = request.args.get('start')
        end = request.args.get('end')
        
        print(username, cat_name, start, end)
        if username != None and cat_name != None and start != None and end != None:
        
            # 貓名 日期範圍選擇     
            df_cat_health_care, allergic_list = cat_health_care_daterange(username, cat_name, start, end, df_cath, df_allergic) 
                
            # #有了字典 轉換 查詢的貓咪健康狀況，所獲得的推薦成份
            Cat_recommend, Cat_harmful, df_product_all, df_cat_health = select_cat_to_recommend_ingredients(df_pro, df_cat_health_care, cat_name, dict_CHC2REC)
            
            # print("keys: ", df_cat_health.keys())
            
            #有了推薦成份，轉換進行推薦演算法公式，獲得產品成分評分表
            Product_Rating_table = Cat_helpful_scores(df_cat_health, df_ingre, Cat_recommend, Cat_harmful, allergic_list, mode=False) 
                
            #推薦演算法的排序檢索 回傳推薦商品
            Product_Recommend_table = Recommend( Product_Rating_table, merge_product, sort_key='評分',therehold=0.2, recommend_num=8 )  
            
            
            # 篩選推薦表的成分
            ingrd_df = Product_Recommend_table.iloc[:, -15:-1].replace('nan', 0)
            ingre_list = []
            temp = []
            for i  in range(ingrd_df.shape[0]): 
                for value  in ingrd_df.iloc[i,:].fillna(0).values.tolist():
                    if value != 0:
                        temp.append(value)
                        
                # print(temp)
                ingre_list.append(temp)
                temp = []

            # print(ingre_list[:3])

            Product_title = Product_Recommend_table['產品名稱'].T.values.tolist()
            Product_phto = Product_Recommend_table['圖片'].T.values.tolist()
            Product_price = Product_Recommend_table['價格'].T.values.tolist()
            Product_age = Product_Recommend_table['適用年齡'].T.values.tolist()

            return render_template('recommend.html', **locals())
        
        else:
            # 這區塊開始隨機推薦
            
            df_cat_health = None
            #有了推薦成份，轉換進行推薦演算法公式，獲得產品成分評分表
            Product_Rating_table = Cat_helpful_scores(None, df_ingre, [], [], [], mode=True) 
                
            #推薦演算法的排序檢索 回傳推薦商品
            Product_Recommend_table = Recommend( Product_Rating_table, merge_product, sort_key='評分',therehold=0.2, recommend_num=8 )  
            
            # 篩選推薦表的成分
            ingrd_df = Product_Recommend_table.iloc[:, -15:-1].replace('nan', 0)
            ingre_list = []
            temp = []
            for i  in range(ingrd_df.shape[0]): 

                for value  in ingrd_df.iloc[i,:].fillna(0).values.tolist():
                    if value != 0:
                        temp.append(value)
                    
                # print(temp)    
                ingre_list.append(temp)
                temp = []

        
            Product_title = Product_Recommend_table['產品名稱'].T.values.tolist()
            Product_phto = Product_Recommend_table['圖片'].T.values.tolist()
            Product_price = Product_Recommend_table['價格'].T.values.tolist()
            Product_age = Product_Recommend_table['適用年齡'].T.values.tolist()
            
            return render_template('recommend.html', **locals())
    except Exception as e:
        dev_logger.error(f"Catch an exception - {e}", exc_info=True)
  
        return render_template('recommend.html', **locals())
        
        


# ##如果是主程式，那就執行....
# if __name__ == '__main__':
#     # 執行 app.run() 函式，執行網頁伺服器的啟動動作
#     app.run(debug=True)




