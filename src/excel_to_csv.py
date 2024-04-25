import pandas as pd

df = pd.read_excel('//data/lj/llm/dataset/iter4/raw_data.xlsx')
df.to_csv('/data/lj/llm/dataset/iter4/raw_data.csv',index = False)