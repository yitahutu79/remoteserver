import json

def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def clean_json_data(data, exclude_words):
    cleaned_data = []
    for item in data:
        if not any(word in item['input'] or word in item['output'] for word in exclude_words):
            cleaned_data.append(item)
    return cleaned_data

def write_cleaned_json_data(cleaned_data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

def main():
    input_filename = '/data/lj/llm/LLaMA-Factory-new/data/train_docqa8000.json'
    output_filename = '/data/lj/llm/LLaMA-Factory-new/data/train_cleaned_docqa8000.json'
    exclude_words = ['初六','过年','年后','春节','新年','初一','初七','初八','初九','年前']

    data = read_json_file(input_filename)
    cleaned_data = clean_json_data(data, exclude_words)
    write_cleaned_json_data(cleaned_data, output_filename)

if __name__ == '__main__':
    main()

