import re
import json
import time
# from datasets import load_dataset


def extract_yes_or_no(text):
    # 匹配 'yes' 或 'no'（忽略大小写）
    match = re.search(r'\b(yes|no)\b', text, re.IGNORECASE)
    
    if match:
        return match.group(0).lower()  # 提取并返回匹配到的 'yes' 或 'no'
    else:
        return None  # 如果未找到，返回 None

def parse_data(data, unique_id):
    data_inputs = data["input"].split('\n\n')
    data_inputs = [item.replace("No or Yes?", "") for item in data_inputs]
    data_inputs = [item.replace("Yes or No?", "") for item in data_inputs]
    data_inputs = [item.replace("Options: - Yes - No", "") for item in data_inputs]
    data_inputs = [item.replace("Options: - No - Yes", "") for item in data_inputs]
    data_inputs = [item.replace("Options:\n- Yes\n- No", "") for item in data_inputs]
    data_inputs = [item.replace("Options:\n- No\n- Yes", "") for item in data_inputs]
    
    qa_pairs = []
    for idx, data_input in enumerate(data_inputs):
        try:
            question = data_input.strip().split("Does")
            question, answer = question[-1].strip().split("?")
            question = f"Does {question}?"
            answer = extract_yes_or_no(answer.strip())
        except Exception as e:
            print(e)
            continue
        
        if question is None or answer is None:
            continue
        
        qa_pair = {
            "id": f"{unique_id}_{idx}",
            "Question": question,
            "Answer": answer,
            "Tags": ["finance"]  # 根据需求添加标签
        }
        qa_pairs.append(qa_pair)
        
    return qa_pairs


if __name__ =="__main__":
    start_time = time.time()

    # 加载 'Headline' 子集
    # dataset = load_dataset("AdaptLLM/finance-tasks", split="Headline")
    with open(r"test.json", "r", encoding="utf-8") as fr_json:
        dataset = json.load(fr_json)

    # 处理整个数据集
    result = []
    for data in dataset:
        parsed_data = parse_data(data, data["id"])
        result.extend(parsed_data)

    # 将结果保存为 JSON 文件
    with open(r"formatted_data.json", "w") as fw_json:
        json.dump(result, fw_json, indent=4)

    end_time = time.time()
    total_time = end_time - start_time

    # 输出统计信息
    print(f"提取的问题-答案对总数: {len(result)}")
    print(f"数据清理和转换花费时间: {total_time:.2f} 秒")
