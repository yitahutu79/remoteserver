import pandas as pd
import random
import json
import os

path = '/data/cxl/dataset/datasets/doc/comprehension_data'
json_files = os.listdir(path)
# 读取所有JSON文件
all_data = []

for file in json_files:  # 遍历文件列表中的每个文件
        if file.split('.')[1] != 'json':  # 如果文件不是以.json结尾的，跳过当前循环
            continue
        json_file = json.load(open(os.path.join(path, file), 'r', encoding='utf-8'))  # 加载当前文件的JSON数据
        data = json_file['data']  # 获取JSON数据中的'data'字段
        for item in data:  # 遍历'data'字段中的每个条目
            paragraphs = item['paragraphs']  # 获取每个条目的'paragraphs'字段
            for item in paragraphs:  # 遍历'paragraphs'字段中的每个条目
                context = item['context']  # 获取当前条目的'context'字段
                qas_list = item['qas']  # 获取当前条目的'qas'字段

                for qas in qas_list:  # 遍历'qas'字段中的每个条目
                    try:
                        json_body = dict()  # 创建一个空字典用于存储处理后的数据
                        question = qas['question']  # 获取当前条目的'question'字段
                        answers = qas["answers"][0]['text']  # 获取当前条目的'answers'字段的第一个条目的'text'字段
                        # 你是一名电商人工客服,现在不是工作时间不要求你用客服语气说话,只是考验你从文档中抽取信息的能力
                        json_body['instruction'] = '下面考验你从文档中抽取信息的能力,请你通过分析文档内容后精简的回答问题。\n 以下是供你参考的已知信息：'+ context +'\n\n你要回复的问题是:'    # 将问题存储在字典中的'instruction'字段中
                        json_body["output"] = answers.replace('\n\n','\n')  # 将答案存储在字典中的'output'字段中，并替换掉多余的换行符
                        json_body["input"] = question  # 将段落内容存储在字典中的'input'字段中
                        json_body["history"] = []  # 创建一个空列表，用于存储历史记录

                        # 根据一些条件进行筛选
                        if len(answers) > 40:  # 如果答案长度大于40，跳过当前循环
                            continue
                        if len(answers) < 10:  # 如果答案长度小于10，跳过当前循环
                            continue
                        if len(context) < 150 or len(context) > 1024:  # 如果段落内容长度小于150，跳过当前循环
                            continue
                        

                        all_data.append(json_body)  # 将处理后的字典添加到结果列表中
                    except:
                        continue  # 如果发生异常，跳过当前循环


# 随机抽取3000条作为测试集
# test_data = random.sample(all_data, 13000)
test_data = '/data/lj/llm/dataset/test_train/test_100.json'
with open(test_data,'r',encoding='utf-8') as f:
    test_data = json.load(f)

# 剩下的作为训练集
rest_data = [item for item in all_data if item not in test_data]
train_data = random.sample(rest_data, 18000)
train_13000 = train_data[:13000]

# 将测试集和训练集保存为新的JSON文件
with open('train_13000.json', 'w', encoding='utf-8') as f:
    json.dump(train_13000, f, ensure_ascii=False, indent=4)

with open('train_18000.json', 'w', encoding='utf-8') as f:
    json.dump(train_data, f, ensure_ascii=False, indent=4)

print(f"Training1 set size: {len(train_13000)}")
print(f"Training2 set size: {len(train_data)}")
