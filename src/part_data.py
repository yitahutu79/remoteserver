import json

def truncate_json(input_file_path, output_file_path, num_elements):
    """
    从输入的JSON文件中截取指定数量的数据元素，并将结果写入输出文件。

    :param input_file_path: 输入的JSON文件路径。
    :param output_file_path: 输出的JSON文件路径。
    :param num_elements: 要截取的数据元素数量。
    """
    try:
        # 读取输入的JSON文件内容
        with open(input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
       # 确保数据是列表类型
        if not isinstance(data, list):
            raise ValueError("输入的JSON不是数组形式。")
        
        # 截取指定数量的数据元素
        truncated_data = data[:num_elements]
         
        # 将截取后的数据写入输出文件
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(truncated_data, file, ensure_ascii=False, indent=4)
    except json.JSONDecodeError:
        # 处理JSON解码错误
        print(f"错误：{input_file_path} 不是有效的JSON文件。")
    except ValueError as e:
        # 处理其他值错误
        print(f"错误：{e}")


# input_file_path = '/data/lj/llm/dataset/test&train/test_data.json'
# output_file_path = '/data/lj/llm/dataset/test&train/test_100.json'
# num_elements_to_keep = 100
input_file_path = '/data/yyb/data_source/from_baidu/output/B copy.json'
output_file_path = '/data/yyb/data_source/from_baidu/output/B_10.json'
num_elements_to_keep = 10

truncate_json(input_file_path, output_file_path, num_elements_to_keep)
