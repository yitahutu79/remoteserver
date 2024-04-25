import pandas as pd
from tqdm import tqdm
from pandas import ExcelWriter
import os
import re
# from cluster import cluster
import keyword_classify

def match(key,s):
    pattern = r'\b' + re.escape(key) + r'\b'
    match_in = re.search(pattern, s) is not None
    return match_in
 
def clear_directory(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            clear_directory(file_path)

def main(kb_path, cluster_num,type,iter_num):
    
    df = pd.read_excel(kb_path)
    df.columns
    #24->57 23->56
    kb2name={
            '0':
                {'3':'沁润-藕粉速溶','4':'沁润-谷物盟主烧仙草粉','5': '沁润-批发专用', '6': '沁润-阿萨姆奶茶粉速溶冲泡家用免煮', 
                 '7': '沁润-椰奶冻粉', '8': '沁润-黄瓜籽粉', '9': '沁润-豆浆粉', '10': '沁润-澳洲进口燕麦片', 
                 '11': '沁润-五彩色面粉果蔬粉', '12': '沁润-奶盖粉', '13': '沁润-黑芝麻糊', '14': '沁润-谷物盟主双皮奶粉', '15': '沁润-谷物盟主布丁粉', 
                 '16': '沁润-杏仁粉', '17': '沁润-小麦胚芽', '19': '沁润-缤纷谷物脆', '21': '恬必忧-香肠调味料',
                 '22':'恬必忧-肠衣','24':'恬必优-粽叶','25':'恬必忧-调味料','26':'恬必优-五香卤蛋调料包','27':'恬必忧-鲜粽叶',
                 '44':'沁润-拉丝酸奶','45':'沁润-红枣粉','46':'沁润-山药百合牛乳','47':'沁润-山药粉','48':'沁润-九红粉'},
            '1':
                {'18': '沁润','23':'恬必优'},
        }
    keys_list = list(kb2name['0'].keys()) + list(kb2name['1'].keys())


    new_dfs = {}
    for key in keys_list:
        new_dfs[key] = pd.DataFrame(columns=df.columns)



    for index, row in tqdm(df.iterrows()):
        flag = 0 # 变成1代表存了
        kb_ids = str(row['kb_ids'])  # 假设列名为 'kb_ids'
        for key in kb2name['0'].keys():
            if match(key,kb_ids):
                new_dfs[key] = pd.concat([new_dfs[key],pd.DataFrame(row).transpose()],axis=0)#([pd.DataFrame(row), new_dfs[value]], ignore_index=True) # .concat(row)#new_dfs[value].append(row)
                flag = 1
                break
        if flag == 1:
            continue
        for key in kb2name['1'].keys():
            if match(key,kb_ids):
                new_dfs[key] = pd.concat([new_dfs[key],pd.DataFrame(row).transpose()],axis=0) # new_dfs[key] = pd.concat([new_dfs[key],row]) 
                
    print('分析完毕')
    
    save_path = os.path.join(os.getcwd(),f"data/post_data/newkb/iter{iter_num}")
    # 若目录不存在，创建目录
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    #第一次调用清空文件夹
    if type == 1:
        # 调用函数并传入要清空的目录路径
        clear_directory(save_path)

    # 对商品进行分类
    for key in tqdm(kb2name['0'].keys()):  
        path = os.path.join(save_path, f"{kb2name['0'][key]}-iter_{iter_num}.xlsx")
        if len(new_dfs[key]) == 0:
            continue
        new_dfs[key].to_excel(path,index=False)

    # 对店铺进行分类
    # 第一种数据处理方法：聚类    
    if (type == 1):
        for key in tqdm(kb2name['1'].keys()):  
            path = os.path.join(save_path,f"{kb2name['1'][key]}(cluester版).xlsx")
            new_dfs[key].to_excel(path,index=False)
            cluster.main(path,cluster_num,kb2name['1'][key],iter_num)
    # 第二种数据处理方法：规则匹配        
    elif (type == 2):
        # 有店铺ID
        for key in tqdm(kb2name['1'].keys()): 
            path = os.path.join(save_path,f"{kb2name['1'][key]}(规则匹配版).xlsx")
            new_dfs[key].to_excel(path,index=False)
            keyword_classify.main(path)
        # ID为空
        blank=pd.DataFrame(columns=df.columns)
        path = os.path.join(save_path,"空白ID.xlsx")
        for index, row in tqdm(df.iterrows()):
            if row['kb_ids'] != row['kb_ids']:
                blank=blank.append(row.transpose(),ignore_index=True)
        blank.to_excel(path,index=False)
        keyword_classify.main(path)
    print(f"存储完毕,新生成的文件路径为{save_path}")
    print(f"存储完毕,新生成的文件内容为{os.listdir(save_path)}")
    
if __name__ == '__main__':
    path='/root/autodl-tmp/lj_workplace/0110/iter/data/post_data/kb_data.xlsx'
    main(path,2,1,3)