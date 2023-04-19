
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from IPython.display import HTML
from pathlib import Path
from datetime import datetime

 
from flask import Flask, redirect, url_for ,request, render_template, Blueprint , jsonify, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy 

#  plotly color https://plotly.com/python/discrete-color/
from view.load_db import load_files
from view.my_log import my_logging
dev_logger = my_logging()

##設定畫圖引擎
plotly.io.json.config.default_engine = 'orjson'

plotly_sample = Blueprint('plotly_sample', __name__)

def show_cat_name_heatmap(username='', cat_name='', start='', end=''):
    """使用者選擇 cat_name 查看 輸出的互動式圖表"""

    _, _, df, _ = load_files()
    
    matrix= df.corr()

    fig = px.imshow(matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
    fig.update_layout(height=500, width=1800, overwrite=True, title_text=f"毛孩健康狀況關聯圖",
                        font = {
                        'size': 20,
                        'family': 'fantasy',
                        'color': '#0099C6'
                        },
                        # hoverlabel = {
                        #     'bgcolor': 'yellow',
                        #     'bordercolor': 'black',
                        #     'namelength': -1,
                        #     'font': {'color': 'black'}
                        # }
    )  
    
    diagram_path = Path('templates') / f"{cat_name}.heatmap.html"
    fig.write_html(diagram_path, include_plotlyjs="cdn")
    # fig.show()

    return diagram_path

def show_cat_name_scatter(username):

    _, _, df_cath, _  = load_files()
    # username = '海雯綺'
    # keys
    keys = df_cath[ df_cath['姓名'] == username]['Pet_Name'].unique() ##['Aegle' 'Tristian' 'Dane']
    # print(keys)
    dict1 = dict()
    for i, key in enumerate(keys):
        dict1[key] = str(i)

    # print(dict1)

    df_cath['which'] = df_cath[ df_cath['姓名'] == username]['Pet_Name'].map(lambda x: dict1[x]).map(int)
    df_cath['體重'] = df_cath['體重'].astype(float)

    category = []
    for key in keys:
        category.append( df_cath[ df_cath['姓名'] == username][ df_cath[ df_cath['姓名'] == username]['Pet_Name'] == key ][[ '小便次數',  '便便數量', '體重', 'which']] )


    fig = make_subplots(rows=1, cols=1)

    for i in range(len(category)):
        fig.add_trace(
            go.Scatter(x=category[i]['小便次數'],
                            y=category[i]['便便數量'],
                            text=category[i]['體重'].astype(float).values,
                            name=keys[i],
                            mode='markers',
                            marker=dict(size=category[i]['體重'].astype(float).values,
                                            sizemode='diameter',
                                            sizeref=category[i]['體重'].astype(float).values.max()/25,
                                            opacity=0.4,
                                            color=px.colors.qualitative.Plotly[i-8],
                                            showscale=False),
                            showlegend=True),
            row=1, col=1
        )


    # X 軸
    fig.update_xaxes(title_text="小便次數", showgrid=True, zeroline=True, showticklabels=True)
    # Y 軸
    fig.update_yaxes(title_text="便便數量", showgrid=True, zeroline=True, showticklabels=True)

    fig.update_layout(height=500, width=1800, overwrite=True, title_text=f"{username}の毛孩 分佈圖",
                        font = {
                        'size': 20,
                        'family': 'fantasy',
                        'color': '#0099C6'
                        },
                        hoverlabel = {
                            'bgcolor': 'yellow',
                            'bordercolor': 'black',
                            'namelength': -1,
                            'font': {'color': 'black'}
                        }
    )  


    diagram_path = Path('templates') / f"{username}.bubble.html"

    fig.write_html(diagram_path, include_plotlyjs="cdn")
    # fig.show()

    return diagram_path

def show_cat_name_pie(username='', cat_name='', start='', end=''):
    """### 使用者選擇 cat_name 日期範圍 查看 輸出的圓餅圖表"""



    _, _, df, _ = load_files()
    # print(df)
    start, end = datetime.strptime(start, '%Y-%m-%d').date(), datetime.strptime(end, '%Y-%m-%d').date()


    date_range_mask = ( df['紀錄日期'] >= start ) & ( df['紀錄日期'] <= end )
    cat_name_mask = ( df['Pet_Name'] == cat_name )
    user_name_mask = ( df['姓名'] == username )
    df_filted = df[ date_range_mask & cat_name_mask & user_name_mask ]


    keys = ['飯量',	'喝水量'
    ,'時常抓癢', '流眼淚', '拉稀',	'嘔吐',	'頻尿'
    ]
    labels = ['0', '1']

    fig = make_subplots(rows=1, cols=7, specs=[[{'type':'domain'}, {'type':'domain'}
    , {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}
    ]])

    for i, key in enumerate( keys ):
    
        if df_filted[[key]].value_counts().values.shape[0] > 1:

            label1 = df_filted[[key]].value_counts().index.values[0][0]    #label
            label2 = df_filted[[key]].value_counts().index.values[1][0]   #label2
            # print(label1, label2)
            fig.add_trace(go.Pie(labels=[label1, label2], values = df_filted[[key]].value_counts().values.tolist(), name=f"{key}"),
                1, i+1)
        
        else:
            label1 = df_filted[[key]].value_counts().index.values[0][0]    #label
            fig.add_trace(go.Pie(labels=[label1], values = df_filted[[key]].value_counts().values.tolist(), name=f"{key}"),
                1, i+1)
            
        # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(
        title_text="健康狀況(0:正常/1:異常)", 
        font = {
                'size': 20,
                'family': 'fantasy',
                'color': 'black'
                },
        # Add annotations in the center of the donut pies.
        annotations=[dict(text=f'{keys[0]}', x=0.035, y=0.9, font_size=15, showarrow=False),
                    dict(text=f'{keys[1]}', x=0.18, y=0.9, font_size=15, showarrow=False)
                    , dict(text=f'{keys[2]}', x=0.355, y=0.9, font_size=15, showarrow=False),
                    dict(text=f'{keys[3]}', x=0.50, y=0.9, font_size=15, showarrow=False),
                    dict(text=f'{keys[4]}', x=0.67, y=0.9, font_size=15, showarrow=False),
                    dict(text=f'{keys[5]}', x=0.82, y=0.9, font_size=15, showarrow=False),
                    dict(text=f'{keys[6]}', x=0.965, y=0.9, font_size=15, showarrow=False)
                    ])

    diagram_path = Path('templates') / f"{cat_name}.pie.html"

    fig.write_html(diagram_path, include_plotlyjs="cdn")
    # fig.show()

    return diagram_path

def show_cat_name_merge(username='', cat_name='', start='', end=''):
    """使用者選擇 cat_name 查看 輸出的互動式圖表"""

 
    _, _, df, _ = load_files()

    # start, end = '2020-01-01', '2022-12-01'
    start, end = datetime.strptime(start, '%Y-%m-%d').date(), datetime.strptime(end, '%Y-%m-%d').date()
    # username = '劉俐彤'
    # cat_name = 'Melany'

    date_range_mask = ( df['紀錄日期'] >= start ) & ( df['紀錄日期'] <= end )
    cat_name_mask = ( df['Pet_Name'] == cat_name )
    user_name_mask = ( df['姓名'] == username )
    df_filted = df[ date_range_mask & cat_name_mask & user_name_mask ]
    fig = make_subplots(rows=3, cols=1)


    # 小便次數範圍版面調整
    fig.add_trace(
        go.Scatter(x = list(df_filted['小便次數'].value_counts().keys()), 
                y= df_filted['小便次數'].value_counts().values,
                text=df_filted['小便次數'].value_counts().values,
                    marker=dict(size= df_filted['小便次數'].value_counts().values,
                                                sizemode='diameter',
                                                sizeref=df_filted['小便次數'].value_counts().values.max()/50,
                                                opacity=0.4,
                                                color=px.colors.qualitative.Plotly[5],
                                                showscale=False),

                    mode = 'markers', #lines+markers+text
                    name = '小便次數頻率'),
        row=2, col=1
    )


    # 便便數量長條圖
    fig.add_trace(
        go.Scatter(x = list(df_filted['便便數量'].value_counts().keys() ), 
                    y= df_filted['便便數量'].value_counts().values,
                    text=df_filted['便便數量'].value_counts().values,
                    marker=dict(size= df_filted['便便數量'].value_counts().values,
                                                sizemode='diameter',
                                                sizeref=df_filted['便便數量'].value_counts().values.max()/50,
                                                opacity=0.4,
                                                color=px.colors.qualitative.Plotly[6],
                                                showscale=False),
                    mode = 'markers',   #markers lines+markers+text
                    name = '便便數量頻率'),
        row=3, col=1
    )

    fig.add_trace(
        go.Scatter(x = df_filted['紀錄日期'], y=df_filted['體重'],
                    marker = {'color': 'green', 'size': 10},
                    mode = 'lines+markers+text', #lines+markers+text
                    name = '體重'),
        row=1, col=1
    )


    # Y 軸
    fig.update_yaxes(title_text="便便頻率", showgrid=True, row=3, col=1)
    fig.update_yaxes(title_text="小便頻率", showgrid=True, row=2, col=1)
    fig.update_yaxes(title_text="體重", showgrid=True, row=1, col=1)

    fig.update_layout(
        height=500, width=1800,overwrite=True, title_text=f"{username} {cat_name} 綜合折線圖",
                        font = {
                        'size': 15,
                        'family': 'fantasy',
                        'color': '#0099C6'
                        },
                        hoverlabel = {
                            'bgcolor': 'yellow', 
                            'bordercolor': 'black',
                            'namelength': -1,
                            'font': {'color': 'black'}
                        }
    )  #dict1=layout


    diagram_path = Path('templates') / f"{cat_name}.merge.html"

    fig.write_html(diagram_path, include_plotlyjs="cdn")
    # fig.show()

    return diagram_path



@plotly_sample.route('/pies/<string:username>/<string:cat_name>/<string:start>/<string:end>',  methods=['GET', 'POST'])
def pies(username, cat_name, start, end):
    ## 互動圖表
    try:
        diagram_path = show_cat_name_pie(username, cat_name, start, end)
        file_name = Path(diagram_path).stem
        # print(file_name)
        return render_template(file_name +'.html', **locals())
    except Exception as e:
        dev_logger.error(f"請檢查使用輸入與plot套件設定!!\nCatch an exception.\n{e}", exc_info=True)
    


@plotly_sample.route('/merge/<string:username>/<string:cat_name>/<string:start>/<string:end>',  methods=['GET', 'POST'])
def merge(username, cat_name, start, end):
    ## 互動圖表
    try:
        diagram_path = show_cat_name_merge( username, cat_name, start, end)
        file_name = Path(diagram_path).stem
        # print(file_name)
        return render_template(file_name +'.html', **locals())
    except Exception as e:
        dev_logger.error(f"請檢查使用輸入與plot套件設定!!\nCatch an exception.\n{e}", exc_info=True)
   

@plotly_sample.route('/scatter/<string:username>',  methods=['GET', 'POST'])
def scatter(username):
    ## 互動圖表
    try:
        # start, end, = '', ''
        diagram_path = show_cat_name_scatter(username)
        file_name = Path(diagram_path).stem
        # print(file_name)
        return render_template(file_name +'.html', **locals())
    except Exception as e:
        dev_logger.error(f"請檢查使用輸入與plot套件設定!!\nCatch an exception.\n{e}", exc_info=True)


@plotly_sample.route('/heatmap',  methods=['GET', 'POST'])
def heatmap():
    ## 互動圖表
    try:
        diagram_path = show_cat_name_heatmap()
        file_name = Path(diagram_path).stem
        # print(file_name)
        return render_template(file_name +'.html', **locals())
    except Exception as e:
        dev_logger.error(f"請檢查使用輸入與plot套件設定!!\nCatch an exception.\n{e}", exc_info=True)

 


