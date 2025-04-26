import re
import csv

def parse_vocabulary(input_filename, output_filename):
    """
    解析单词本文件，将数据导入到 CSV 文件中，并处理长中文解释。

    Args:
        input_filename (str): 单词本文件名（.txt）。
        output_filename (str): 输出 CSV 文件名（.csv）。
    """
    word_data = []
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            content = infile.read()
            entries = content.strip().split('\n\n')
            for entry in entries:
                lines = entry.strip().split('\n')
                if len(lines) >= 3:
                    word = lines[0].strip()
                    pronunciation = lines[1].strip()
                    definitions = []
                    for line in lines[2:]:
                        match = re.match(r'([a-z.]+)\s+(.*)', line.strip())
                        if match:
                            pos = match.group(1)
                            explanation = match.group(2).strip()
                            definitions.append({'pos': pos, 'explanation': explanation})
                    word_data.append({'word': word, 'pronunciation': pronunciation, 'definitions': definitions})
    except FileNotFoundError:
        print(f"错误：找不到文件 '{input_filename}'")
        return

    all_words = []
    for item in word_data:
        word = item['word']
        pronunciation = item['pronunciation']
        for definition in item['definitions']:
            pos = definition['pos']
            explanation = definition['explanation']

            # 处理长中文解释
            if len(explanation.encode('utf-8')) > 16:
                explanation_parts = []
                current_part = ""
                for char in explanation:
                    if len((current_part + char).encode('utf-8')) <= 16:
                        current_part += char
                    else:
                        explanation_parts.append(current_part)
                        current_part = char
                if current_part:
                    explanation_parts.append(current_part)
                for i, part in enumerate(explanation_parts):
                    if i == 0:
                        all_words.append([word, pronunciation, pos, part])
                    else:
                        all_words.append([word, pronunciation, pos, part, "续"]) # 标记为续行
            else:
                all_words.append([word, pronunciation, pos, explanation])

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['单词', '音标', '词性', '中文解释', '备注']) # 写入表头
            writer.writerows(all_words)
        print(f"成功将 {len(word_data)} 个单词解析并导出到 '{output_filename}'")
    except Exception as e:
        print(f"导出 CSV 文件时发生错误：{e}")

    print(f"单词数量：{len(word_data)}")

if __name__ == "__main__":
    input_file = r"goo_word2xls_v3_wd\词汇-01-自然地理.txt"  # 您的单词本文件名
    output_file = r"goo_word2xls_v3_wd\自然地理词汇.xlsx"  # 您希望保存的 Excel 文件名
    parse_vocabulary(input_file, output_file)