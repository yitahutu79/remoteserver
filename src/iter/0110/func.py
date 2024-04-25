import json
from typing import Optional
import requests
import pandas as pd
 
def _retrieval_test_init():
    base_url = 'http://localhost:8008/kb_retrieval_test_init'
    response = requests.post(base_url, json={})
    res = response.text
    print(res)
    return res

def _retrieval_test_query(query, topk=5, kb_ids: list=None) -> Optional[list]:
    base_url = 'http://localhost:8008/kb_retrieval_test_query'
    response = requests.post(base_url, json={
        'query': query, 
        'topk': topk,
        'kb_ids': kb_ids,
    })
    
    retrieved_items = response.json()["data"]
    # print(retrieved_items)
    return retrieved_items

def _retrieval_test_close():
    base_url = 'http://localhost:8008/kb_retrieval_test_close'
    response = requests.post(base_url, json={})
    res = response.text
    print(res)
    return res

def model_recall(query):
    
    _retrieval_test_init()

    for _ in range(1):

        message = _retrieval_test_query(query, 20, ['49','51','52','53'])[:20]
        message = [x['context'] for x in message]
        return message
    _retrieval_test_close()
   

def fun10(json_path):
    with open(json_path) as v4_file:
        v4 = json.load(v4_file)
        # print(v4)
        # time.sleep(10000)
        for row in v4:
            ins = row['instruction']
            doc = str(model_recall(ins)) # 替换为召回函数
            
            print(doc)
            prompt = (
                '你是一名电商客服，你的任务是参考已知信息解答用户的疑问，用礼貌、专业的态度进行回答。请务必使用中文回答\n以下是供你参考的已知信息或是问答模板：\n'
                + doc
                + '\n以上信息可能与用户的问题无关，你需要根据用户的具体需求选择性的参考。'
            )
            row['input'] = prompt
    with open(json_path, 'w',encoding = 'utf8') as v4_file:
        json.dump(v4, v4_file, ensure_ascii=False)

if __name__=="__main__":
    json_path ='/root/autodl-tmp/lj_workplace/0110/V4_total.json'
    fun10(json_path)