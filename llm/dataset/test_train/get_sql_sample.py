import pandas as pd
import pymysql
from datetime import datetime, timedelta
import random
import json

# 计算近一周的日期范围
now = datetime.now()
one_week_ago = now - timedelta(weeks=1)
end_date = now.strftime('%Y-%m-%d %H:%M:%S')
start_date = one_week_ago.strftime('%Y-%m-%d %H:%M:%S')

# 使用pymysql连接到MySQL数据库
pro_conn = pymysql.connect(
    host='119.188.67.206',
    user='airead',
    password='2fb0df449700f431723cfb1cd7525baf',
    database='e_chatbot_prod',
    charset='utf8mb4'
)

# 构造SQL查询语句，获取近一周的数据
col_name = ['q','que','ai_answer','actual_send_answer','kb_ids','new_refer','order_status','refund_status']
sql = f"""
SELECT que, ai_answer, actual_send_answer, refer_content, create_time, customer_origin_id, member_id, kb_ids, goods_name, order_status, refund_status
FROM trade_ai_log
WHERE create_time > '{start_date}' AND create_time < '{end_date}'
AND kb_ids IN (18)
ORDER BY create_time DESC
"""

# 读取数据
data = pd.read_sql(sql, pro_conn)
data_tmp = data.copy()
bad_idx = list()

for idx, row in data.iterrows():
    # with query
    que = row['que']
    if que == '[]':
        bad_idx.append(idx)
        continue
    query = json.loads(que)[-1]['content']
    if query == '':
        bad_idx.append(idx)
        continue
    
    # with doc
    recall = row['refer_content']
    if recall is None:
        docs = ''
        bad_idx.append(idx)
    else:
        recall = json.loads(recall)
        docs = [doc['context'].replace('\n', '') for doc in recall]

    # with actual
    ai_answer = row['ai_answer']
    actual_send_answer = row['actual_send_answer'].replace('\n', '')
    if actual_send_answer is None:
        bad_idx.append(idx)

    order_status = row['order_status']
    refund_status = row['refund_status']

    data_tmp.loc[idx, 'q'] = query
    data_tmp.loc[idx, 'que'] = que
    data_tmp.loc[idx, 'new_refer'] = str(docs)
    data_tmp.loc[idx, 'actual_send_answer'] = actual_send_answer
    data_tmp.loc[idx, 'order_status'] = order_status
    data_tmp.loc[idx, 'refund_status'] = refund_status
data_out = data_tmp[col_name].drop(index=bad_idx)

# 检查数据行数
num_rows = data_out.shape[0]
print("过滤前数据行数为：",num_rows)

# 关闭数据库连接
pro_conn.close()

# 将结果保存到文件
csv_path = '/data/lj/llm/dataset/iter5/newlog.csv'  
data_out.to_csv(csv_path, index=False)

# 读取CSV文件
df_csv = pd.read_csv(csv_path)

# 读取JSON文件
train_data = '/data/lj/llm/LLaMA-Factory-new/data/cleaned_13000.json'
with open(train_data,'r',encoding='utf-8') as f:
    train_data = json.load(f)

# 创建一个列表来存储要过滤的CSV行的索引
to_filter = []

# 遍历JSON文件中的每个条目，检查`input`字段是否与CSV中的`q`列匹配
for item in train_data:
    if item['input'] in df_csv['q'].values:
        to_filter.append(df_csv[df_csv['q'] == item['input']].index.tolist())

# 将所有匹配的索引组合成一个列表
all_filtered_indices = [item for sublist in to_filter for item in sublist]

# 提取过滤掉的CSV数据
df_to_drop = df_csv.loc[all_filtered_indices]
df_to_drop.drop_duplicates(keep='first', inplace=True)

# 保存过滤掉的CSV文件
to_drop_csv_path = '/data/lj/llm/dataset/iter5/dropped_out_data.csv'
df_to_drop.to_csv(to_drop_csv_path, index=False)
num_rows = df_to_drop.shape[0]
print("过滤的数据行数为：",num_rows)
print(f"Filtered out data saved to {to_drop_csv_path}")

# 过滤后的CSV文件
df_filtered = df_csv.drop(df_csv.index[all_filtered_indices])

# 检查数据行数
num_rows = df_filtered.shape[0]
print("过滤后数据行数为：",num_rows)

# 保存过滤后的CSV文件
filtered_csv_path = '/data/lj/llm/dataset/iter5/filtered_data.csv'
df_filtered.to_csv(filtered_csv_path, index=False)

# # 选择随机记录
# if num_rows < 400:
#     # 如果数据行数小于400，选择所有数据
#     sampled_data = data_out
# else:
#     # 如果数据行数大于或等于400，随机选择400条记录
#     sampled_data = data_out.sample(n=400)

print(f"Data saved to {filtered_csv_path}")
