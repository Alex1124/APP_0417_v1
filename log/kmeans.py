import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
import plotly.graph_objs as pgo
from view.load_db import load_files

df_pro, df_ingre, df_cath, df_allergic  = load_files()
username = '海雯綺'
# keys
keys = df_cath[ df_cath['姓名'] == username]['Pet_Name'].unique()
# category
dict1 = dict(Aegle='0', Tristian='1', Dane='2')
print(dict1)
df_cath['which'] = df_cath[ df_cath['姓名'] == username]['Pet_Name'].map(lambda x: dict1[x])
# print(df_cath[ df_cath['姓名'] == username]['Pet_Name'])
print(df_cath[ df_cath['姓名'] == username]['which'].shape)

category = []
for key in keys:
    category.append( df_cath[ df_cath['姓名'] == username][ df_cath[ df_cath['姓名'] == username]['Pet_Name'] == key ][[ '小便次數',  '便便數量', 'which']].values )

print(category)


new_user_cats_df = df_cath[ df_cath['姓名'] == username][[ '小便次數',  '便便數量', '體重','which']] 
print(f"{username} cat df :\n{new_user_cats_df}")

import numpy as np

X = np.vstack( (category))

print(X.shape)
Y = X[:, -1]
X = X[:, 0:2]
# print(X.shape,Y.shape)

silhouette_avg = []

kmeans = KMeans(n_clusters= 3, max_iter=9000, random_state=0)
kmeans.fit(X)
y_predict =kmeans.predict(X)
# Y[Y == 1] = 2
# Y[Y == 0] = 1
# Y[Y == 2] = 0
print(Y)
print(y_predict)
silhouette_avg.append(accuracy_score(Y, y_predict)) 


print(silhouette_avg)
print(kmeans.labels_)
print(kmeans.cluster_centers_)





# Represent neighborhoods as in previous bubble chart, adding cluster information under color.
trace0 = pgo.Scatter(x=X[0],
                     y=X[1],
                     text=np.arange(X.shape[0]),
                     name='',
                     mode='markers',
                     marker=pgo.Marker(size=new_user_cats_df['體重'].values,
                                       sizemode='diameter',
                                       sizeref=new_user_cats_df['體重'].values.max()/50,
                                       opacity=0.5,
                                       color=y_predict),
                     showlegend=False
)



# Represent cluster centers.
trace1 = pgo.Scatter(x=kmeans.cluster_centers_[:, 0],
                     y=kmeans.cluster_centers_[:, 1],
                     name='',
                     mode='markers',
                     marker=pgo.Marker(symbol='x',
                                       size=12,
                                       color=range(3)),
                     showlegend=False
)
data7 = pgo.Data([trace0, trace1])

layout5 = pgo.Layout(title='cat kmeans',
                     xaxis=pgo.XAxis(showgrid=False,
                                     zeroline=False,
                                     showticklabels=False),
                     yaxis=pgo.YAxis(showgrid=False,
                                     zeroline=False,
                                     showticklabels=False),
                     hovermode='closest'
)
layout7 = layout5
layout7['title'] = 'cat kmeans'
fig7 = pgo.Figure(data=data7, layout=layout7)
fig7.show()

# indArr,peak_heightsDict=find_peaks(silhouette_avg)

# # 在silhouette_avg這個list中，最高點index為三，最佳分群數為5
# RowNumCategories=indArr[0]+2

# # 模型預測及畫圖
# kmeansmodel = KMeans(n_clusters= RowNumCategories, init='k-means++')
# y_kmeans= kmeansmodel.fit_predict(X)

# # 利用joblib 來將模型儲存
# dump(kmeansmodel, 'kmean.joblib') 