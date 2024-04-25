import json
import os
import re
import time
from datetime import datetime
import pandas as pd
import pymysql
from tqdm import tqdm
"""
从数据库中拿数据
过滤
写入到文件。列名为
	Unnamed: 0	que	refer_content	ai_answer	actual_send_answer	kb_ids	create_time	shop_url	member_id
"""

class db_log():
    
    # def __init__(self):
    #     self.
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

    # today = datetime.now().strftime('%Y-%m-%d')
    def read_file(self,excluding_dir):
        # 读文件夹下的每一个文件
        file_ls = []
        excluding_query = list()
        for root, dirs, files in os.walk(excluding_dir):
            for file in files:
                if file.endswith('.xlsx') or file.endswith('.xls'):
                    file_path = os.path.join(root, file)
                    kb = pd.read_excel(file_path, engine='openpyxl')  # 读取Excel文件
                    print(f"Read {file}:")
                    excluding_query.append(kb)
        return excluding_query

    def knowledge_update(self, db_connect, save_path, excluding_dir=None):
        today = datetime.now().strftime('%Y-%m-%d')
        start = time.time()

        # 从数据库读数据
        
        col_name = ['q', 'que', 'refer_content', 'ai_answer', 'a', 'create_time','kb_ids']
        sql = (
            'select que, ai_answer, actual_send_answer, refer_content, create_time, customer_origin_id, member_id, kb_ids '
            'from trade_ai_log '
            'where create_time > \'2024-04-09 00:00:00\' and create_time < \'2024-04-15 24:00:00\''
            'and member_id <> 17 '
            'and member_id <> 18 '
            'and member_id <> 19 '
            
            'order by create_time desc '
        )
        data_log = pd.read_sql(sql, db_connect)
        data_tmp = data_log.copy()
        filter_rows = pd.DataFrame(columns=col_name)
        print(data_log.keys())
        bad_idx = list()
        filter_idx = list()
        dba_list = list()

        # query 过滤
        q_filter = r'OK|啊|。。|我知道|亲|好|哦|谢谢|你好|hi|hello|您好|在吗|嗨|嗯|噢|喔|ok|行|明白|对|客气'
        q_filter2 = r'发货|春节|拼单成功|年前|返现|奖励|评价有礼|过年'
        a_filter = r'\?|好的|是的|是的|对的|嗯嗯|客气|可以的'
        a_filter2 = r'感谢您的光临，祝您生活愉快，再见!'
       
        excluding_query = list()
        if excluding_dir:
            excluding_query=self.read_file(excluding_dir)
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

            if (actual_send_answer == ai_answer
                    or re.search('http', query)):
                bad_idx.append(idx)
                continue
            # -------------------------------     
            # 知识库问题及答案相似度过滤
            
            if len(excluding_query) > 0:
                cnt = 0
                for kb in excluding_query:
                    if 'q' not in kb.columns:
                        kb = kb.rename(columns={'que':'q'})
                    if 'a' not in kb.columns:
                        kb = kb.rename(columns={'actual_send_answer':'a'})
                    # kb.drop_duplicates(subset='q', inplace=True)
                    qa_dict1 = {query : actual_send_answer}
                    qa_dict2 = dict(zip(kb['q'],kb['a']))
                    seen = set()
                    for q in kb['q']:
                        q = str(q)
                        if idx in bad_idx:
                            continue
                        if actual_send_answer == '':
                            bad_idx.append(idx)
                            continue
                        if q == query: 
                            if (q,qa_dict1[q],qa_dict2[q]) in seen:
                                bad_idx.append(idx)
                                continue
                            if qa_dict1[q] != qa_dict2[q]:
                                seen.add((q,qa_dict1[q],qa_dict2[q]))
                                print('@' * 50,"知识库相同问题",'@' * 50)
                                print("问题是：",query)
                                print("答案是：",qa_dict1.get(query),"\n知识库对应答案是：",qa_dict2[q])
                                filter_idx.append(idx)
                                dba_list.append(qa_dict2[q])
                            else:
                                bad_idx.append(idx)
                   
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

            # 未被筛掉的数据做一定的修饰
            data_tmp.loc[idx, 'q'] = query
            data_tmp.loc[idx, 'que'] = que
            data_tmp.loc[idx, 'refer_content'] = str(docs)
            data_tmp.loc[idx, 'a'] = actual_send_answer
        filter_rows = data_tmp[col_name].loc[filter_idx]
        filter_rows['dba'] = dba_list
        filter_rows.to_excel('/data/lj/src/iter/data/dba/0409-0415dba.xlsx', index = False)
        data_out = data_tmp[col_name].drop(index=bad_idx)
        data_out.to_excel(save_path, index = False)
        print(f'len of data: {len(data_out[col_name[0]])}, cost {time.time() - start} seconds')



def main(save_path:str,excluding_dir:str = None):
    """
    excluding_dir 暂时没有使用
    """
    adb = db_log()
    adb.knowledge_update(db_log.pro_conn, save_path, excluding_dir)
    df = pd.read_excel(save_path)
    df.to_excel(save_path, index = False)
    print('kb data process done----')




if __name__ == '__main__':
    db_data_savepath = '/data/lj/src/iter/data/pre_data/0409-0415kb_data.xlsx'# data/post_data/kb_update_' + datetime.now().strftime('%Y-%m-%d') + '.xlsx'
    excluding_dir = '/data/lj/src/iter/data/kb_data' #  已经存进知识库的文件的过滤，暂时没用
    main(db_data_savepath,excluding_dir)