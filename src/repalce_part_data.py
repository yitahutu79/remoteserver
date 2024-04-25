import pandas as pd

# 路径到包含500条数据的文件
csv_500_path = '/data/lj/llm/dataset/iter4/raw_data.csv'

# 路径到包含200条数据的文件
csv_200_path = '/data/lj/llm/dataset/iter5/200log.csv'

# 读取两个文件
df_500 = pd.read_csv(csv_500_path)
df_200 = pd.read_csv(csv_200_path)

# 合并两个DataFrame
df_merged = pd.concat([df_200,df_500.iloc[200:]], axis=0)

# 保存修改后的数据到新的文件
modified_csv_path = '/data/lj/llm/dataset/iter5/raw_data.csv'
df_merged.to_csv(modified_csv_path, index=False)

print(f"Data replaced and saved to {modified_csv_path}")
