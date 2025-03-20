#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt

# 1. 加载数据
# 请确保文件名和路径正确
df = pd.read_csv('BOT_REQUEST.csv')

# 显示前几行数据以确认结构
print("数据预览：")
print(df.head())

# 假设数据中有以下列：'username', 'page', 'thread'
# 若实际列名不同，请相应修改

# 2. 初始化网络图
G = nx.Graph()

# 将所有唯一的编辑者添加为节点
unique_users = df['username'].unique()
for user in unique_users:
    G.add_node(user)
    
# 3. 构建边
# 根据 'page' 和 'thread' 进行分组
grouped = df.groupby(['page', 'thread'])
for (page, thread), group in grouped:
    # 获取该组内所有独立的编辑者
    users_in_group = group['username'].unique()
    # 对于组内任意两个编辑者，构建或更新边
    for user1, user2 in combinations(users_in_group, 2):
        if G.has_edge(user1, user2):
            # 更新已有边：增加权重并添加当前上下文
            G[user1][user2]['weight'] += 1
            G[user1][user2]['contexts'].append((page, thread))
        else:
            # 新建边，并初始化权重和上下文信息
            G.add_edge(user1, user2, weight=1, contexts=[(page, thread)])

# 输出网络摘要信息
print("\n网络摘要：")
print("节点数量（编辑者数）：", G.number_of_nodes())
print("边的数量（社交连接数）：", G.number_of_edges())

# 4. 可视化网络（仅适用于较小的网络，否则图形会过于混乱）
plt.figure(figsize=(8,8))
pos = nx.spring_layout(G, seed=42)  # 固定布局以保证可重复性
nx.draw(G, pos, with_labels=True, node_size=300, font_size=8)
plt.title("Wikidata 编辑者社交网络")
plt.show()

