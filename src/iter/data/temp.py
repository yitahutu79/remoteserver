import pandas as pd
from tqdm import tqdm
from pandas import ExcelWriter
import os

df = pd.read_excel('/root/autodl-tmp/cxl_workspace/com/recall/base_func/iter/data/post_data/kb_data.xlsx')
df.columns

kb2name={
        '0':
            {'19':'恬必优 - 恬必优调味料','24':'恬必优 - 精品天然肠衣','35': '沁润 - 藕粉速溶奇亚籽桂花燕窝茉莉红枣银耳坚果木糖醇玫瑰', '36': '沁润 - 澳洲进口燕麦片', '37': '沁润 - 杏仁七白饮杏仁粉无添加烘焙银耳美南杏仁粉白营养', '38': '沁润 - 谷物盟主双皮奶粉', '39': '沁润 - 批发专用', '41': '沁润 - 小麦胚芽', '44': '沁润 - 黄瓜籽粉', '45': '沁润 - 椰奶冻粉免煮型椰奶专用', '46': '沁润 - 奶盖粉', '47': '沁润 - 豆浆粉', '48': '沁润 - 五彩色面粉果蔬粉', '49': '沁润 - 缤纷谷物脆', '51': '沁润 - 谷物盟主布丁粉', '53': '沁润 - 阿萨姆奶茶粉速溶冲泡家用免煮', '54': '沁润 - 谷物盟主烧仙草粉', '55': '沁润 - 黑芝麻糊黑芝麻核桃黑豆黑米桑葚粉'}
,
        '1':
            {'33': '沁润','23':'恬必优'},
    }
keys_list = list(kb2name['0'].keys()) + list(kb2name['1'].keys())


new_dfs = {}
for key in keys_list:
    new_dfs[key] = pd.DataFrame(columns=df.columns)



for index, row in tqdm(df.iterrows()):
    flag = 0 # 变成1代表存了
    kb_ids = str(row['kb_ids'])  # 假设列名为 'kb_ids'
    for key in kb2name['0'].keys():
        if key in kb_ids:
            new_dfs[key] = pd.concat([new_dfs[key],pd.DataFrame(row).transpose()],axis=0)#([pd.DataFrame(row), new_dfs[value]], ignore_index=True) # .concat(row)#new_dfs[value].append(row)
            flag = 1
            break
        if flag == 1:
            break
    for key in kb2name['1'].keys():
        if key in kb_ids:
            new_dfs[key] = pd.concat([new_dfs[key],row]) 
            
print('分析完毕')
            
for key in tqdm(kb2name['0'].keys()):  
    path = os.path.join(os.getcwd(),f"post_data/temp/{kb2name['0'][key]}.xlsx")
    new_dfs[key].to_excel(path,index=False)
for key in tqdm(kb2name['1'].keys()):  
    path = os.path.join(os.getcwd(),f"post_data/temp/{kb2name['1'][key]}.xlsx")
    new_dfs[key].to_excel(path,index=False)
print('存储完毕')
#           
            
