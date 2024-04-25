import json
import os,sys
import re
import time
from datetime import datetime
import pandas as pd
import pymysql
import difflib
import glob
from tqdm import tqdm
"""
从数据库中拿数据
过滤
写入到文件。列名为
	Unnamed: 0	que	refer_content	ai_answer	actual_send_answer	kb_ids	create_time	shop_url	member_id
"""

class db_log():
    
    
    def __init__(self):
        start_time = '2024-02-19 00:00:00'
        end_time = '2024-02-19 24:00:00'
        
    test_conn = pymysql.connect(
        host='39.107.112.208',
        user='e_chatbot',
        database='e_chatbot_dev',
        password='CpYnSAniC3RwtsnB'
    )
    
    pro_conn = pymysql.connect(
        host='59.110.172.164',
        user='root',
        password='jkhl@2022',
        database='e_chatbot'
        # charset='utf-8'
    )
    def similarity(self,a, b):
        return difflib.SequenceMatcher(None, a, b).ratio()
    # today = datetime.now().strftime('%Y-%m-%d')
    def read_file(self,excluding_dirs):
        # 读文件夹下的每一个文件
        file_ls = []
        excluding_query = list()
        for excluding_dir in excluding_dirs:
            for root,folder_nmses,file_names in os.walk(excluding_dir):
                for file_name in file_names:
                    file_path = root+os.sep+file_name
                    file_ls.append(file_path)
                    file_ls=[file for file in file_ls if file.endswith('.xlsx')]
    
            for file in file_ls:
                kb = pd.read_excel(file)
                excluding_query.append(kb)
            print(file_ls)
        return excluding_query
    
    def knowledge_update(self, db_connect, save_path,excluding_dir=None):
        today = datetime.now().strftime('%Y-%m-%d')
        start = time.time()

        # 从数据库读数据
        
        col_name = ['q', 'que', 'refer_content', 'ai_answer', 'a', 'create_time','kb_ids']
        sql = (
            'SELECT que, ai_answer, actual_send_answer, refer_content, create_time, customer_origin_id, member_id, kb_ids '
            'FROM trade_ai_log '
            'WHERE create_time > \'{}\' AND create_time < \'{}\''
            ' AND member_id NOT IN (17, 18, 19) '
            'ORDER BY create_time DESC'
        )

        sql = sql.format(self.start_time, self.end_time)
        data_log = pd.read_sql(sql, db_connect)
        print('**init number',len(data_log))
        
        data_tmp = data_log.copy()
        print(data_log.keys())
        bad_idx = list()

        # query 过滤
        q_filter = r'OK|啊|。。|我知道|亲|好|哦|谢谢|你好|hi|hello|您好|在吗|嗨|嗯|噢|喔|ok|行|明白|对|客气'
        q_filter2 = r'发货|春节|拼单成功|年前|快递|指定|能发|返现|奖励|评价有礼|过年'
        a_filter = r'\?|好的|是的|是的|对的|嗯嗯|客气|可以的|备注'
        a_filter2 = r'发货|感谢您的光临，祝您生活愉快，再见!'
        
        q_filter2 = r'春节|年前|过年|年后'
       
        excluding_query = list()
        file_ls=[]
        if excluding_dir:
            excluding_query=self.read_file(excluding_dir)
        
        print('本文档相似度过滤整理数据')
        for i in tqdm(range(len(data_log))):
            break # 暂时不用这些
            for j in range(i+1, len(data_log)):
                row = data_log.iloc[i]
                row2 = data_log.iloc[j]

                # with query
                que = row['que']
                que2 = row2['que']
                if que == '[]':
                    bad_idx.append(i)
                    continue
                query = json.loads(que)[-1]['content']
                query2 = json.loads(que2)[-1]['content']
                if query == '':
                    bad_idx.append(i)
                    continue

            
                # with actual
                ai_answer = row['ai_answer']
                actual_send_answer = row['actual_send_answer'].replace('\n', '')
                ai_answer2 = row2['ai_answer']
                actual_send_answer2 = row2['actual_send_answer'].replace('\n', '')

                # -------------------------------     
                # 本文档相似度过滤
                
                qa_dict1 = {query : actual_send_answer}
                qa_dict2 = {query2 : actual_send_answer2}
                if i in bad_idx:
                    continue
                if actual_send_answer == '':
                    bad_idx.append(i)
                    continue
                if actual_send_answer2 == '':
                    bad_idx.append(j)
                    continue
                if (actual_send_answer == ai_answer
                    or (len(query) < 4 and re.search(q_filter, query))
                    or re.search(q_filter2, query)
                    or re.search('http', query)
                    # or len(query) < 4
                    # or len(actual_send_answer) < 3
                    # or re.search(a_filter2, actual_send_answer)
                    # or (len(actual_send_answer) < 6 and re.search(a_filter, actual_send_answer))
                    ):
                    bad_idx.append(i)
                    continue
                if self.similarity(query, query2) > 0.3 and self.similarity(qa_dict1[query],qa_dict2[query2]) > 0.6:
                    print('*' * 30,"该文档相似问题过滤",'*' * 30)
                    print("问题是：",query, "相似问题是:",query2)
                    print("问题相似度是：",self.similarity(query,query2))
                    print("答案是：",qa_dict1.get(query,'unknow'),"\n相似问题对应答案是：",qa_dict2[query2])
                    print("答案相似度是：",self.similarity(qa_dict1.get(query,'unknow'),qa_dict2[query2]))
                    bad_idx.append(j)
                    continue


        for idx, row in tqdm(data_log.iterrows()):
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
            else:
                recall = json.loads(recall)
                docs = [doc['context'].replace('\n', '') for doc in recall]

            # with actual
            ai_answer = row['ai_answer']
            actual_send_answer = row['actual_send_answer'].replace('\n', '')

            # if ( # actual_send_answer == ai_answer
            #         # or (len(query) < 6 and re.search(q_filter, query))
            #         # or re.search(q_filter2, query)
            #          re.search('http', query)
            #         or re.search('http', actual_send_answer)
            #         or actual_send_answer == '' or actual_send_answer == 'nan'
            #         or len(actual_send_answer) < 2
            #         or len(query) < 2
            #         or re.search(a_filter2, actual_send_answer) # q_filter2 = r'春节|年前|过年|年后
            #         # or (len(actual_send_answer) < 6 and re.search(a_filter, actual_send_answer))
            #         ):
            #     bad_idx.append(idx)
            #     continue
            # -------------------------------     
            # 知识库问题及答案相似度过滤
            if len(excluding_query) > 0:
                cnt = 0
                for kb in excluding_query:
                    if 'q' not in kb.columns:
                        kb = kb.rename(columns={'que':'q'})
                    if 'a' not in kb.columns:
                        kb = kb.rename(columns={'actual_send_answer':'a'})
                    kb.drop_duplicates(subset='q', inplace=True)
                    qa_dict1 = {query : actual_send_answer}
                    qa_dict2 = dict(zip(kb['q'],kb['a']))
                    for q in kb['q']:
                        if idx in bad_idx:
                            continue
                        if actual_send_answer == '':
                            bad_idx.append(idx)
                            continue
                        if q == query and self.similarity(qa_dict1.get(query),qa_dict2[q]) > 0.75:
                            print('*' * 30,"相同问题过滤",'*' * 30)
                            print("问题是：",query)
                            print("答案是：",qa_dict1.get(query),"\n知识库对应答案是：",qa_dict2[q])
                            print("答案相似度是：",self.similarity(qa_dict1.get(query),qa_dict2[q]))
                            bad_idx.append(idx)
                            continue
                        if self.similarity(q,query) > 0.3 and self.similarity(qa_dict1.get(query),[qa_dict2.get(q)]) > 0.6:
                            print('*' * 30,"相似问题过滤",'*' * 30)
                            print("问题是：",query,"\n知识库相似问题是：",q)
                            print("问题相似度是：",self.similarity(q,query))
                            print("答案是：",qa_dict1.get(query),"\n知识库对应答案是：",qa_dict2[q])
                            print("答案相似度是：",self.similarity(qa_dict1.get(query),qa_dict2[q]))
                            bad_idx.append(idx)
                            continue
          
            # 未被筛掉的数据做一定的修饰
            data_tmp.loc[idx, 'q'] = query
            data_tmp.loc[idx, 'que'] = que
            data_tmp.loc[idx, 'refer_content'] = str(docs)
            # data_tmp.loc[idx, 'actual_send_answer'] = actual_send_answer
            data_tmp.loc[idx, 'a'] = actual_send_answer
            
        # 去掉空的和规则的
        data_out = data_tmp[col_name].drop(index=bad_idx)
        # 去掉重复行了
        # data_out.drop_duplicates(subset='q', inplace=True)
        if save_path.endswith('csv'):
            data_out.to_csv(save_path)
        elif save_path.endswith('xlsx'):
            data_out.to_excel(save_path)
        


def main(save_path:str,excluding_dir:str = None,starttime = '2024-02-19 00:00:00' ,endtime = '2024-02-19 24:00:00'):
    """
    输入时间 最后的时间等
    """
    adb = db_log()
    start = time.time()
    adb.start_time = starttime
    adb.end_time = endtime
    
    
    # excluding_dir = 'prod_kb/tianbiyou'

    # save_path = 'knowledge_update/kb_update_' + today + '.xlsx'
    # adb.knowledge_update(db_log.test_conn, save_path, excluding_dir)
    # df1 = pd.read_excel(save_path)
    
    adb.knowledge_update(db_log.pro_conn, save_path, excluding_dir)
    if save_path.endswith('csv'):
        df2 = pd.read_csv(save_path)
        df2.drop_duplicates(subset='q', inplace=True)
        df2.to_csv(save_path)
        
    elif save_path.endswith('xlsx'):
        df2 = pd.read_excel(save_path)
        df2.drop_duplicates(subset='q', inplace=True)
        df2.to_excel(save_path)
        # df2.to_excel('./data/test.xlsx')
        
    
    # pd.concat([df1, df2]).to_excel(save_path)
    print(f'len of data: {len(df2)}, cost {time.time() - start} seconds')

    print('kb data process done----')




if __name__ == '__main__': 
    db_data_savepath = './data/dbdata-219_2.csv' # data/post_data/kb_update_' + datetime.now().strftime('%Y-%m-%d') + '.xlsx'
    # excluding_dir = None #  已经存进知识库的文件的过滤，暂时没用
    # excluding_dir = ['/home/lj/doc/new']
    excluding_dir = None # ['/home/lj/doc/new/恬必忧','/home/lj/doc/new/沁润']
    main(db_data_savepath,excluding_dir,starttime = '2024-02-03 00:00:00' ,endtime = '2024-02-09 24:00:00')

