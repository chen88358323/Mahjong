import re
import csv

def parse_vocabulary_file(input_file, output_file):
    """
    解析单词本文件，并将其内容保存到 CSV 文件中。

    Args:
        input_file (str): 单词本文件名。
        output_file (str): 输出 CSV 文件名。
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正则表达式匹配单词、音标和释义
        entries = re.findall(r'(\S+)\s+/(.*?)/\s+(.+?)(?=\s+\S+\s+/|\Z)', content, re.DOTALL)

        if not entries:
            print("未找到匹配的单词条目。请检查文件格式。")
            return

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Word', 'Pronunciation', 'Definition'])  # 写入标题行
            for entry in entries:
                word, pronunciation, definition = entry
                writer.writerow([word, pronunciation, definition.strip()])  # 写入数据行

        print(f"数据已成功保存到 {output_file}")
        print(f"单词数量: {len(entries)}") #打印单词数量

    except FileNotFoundError:
        print(f"找不到文件 {input_file}")
    except Exception as e:
        print(f"发生错误：{e}")

# 示例用法
input_filename = 'vocabulary.txt'  # 请替换为您的单词本文件名
output_filename = 'vocabulary.csv'  # 请替换为您想要的 CSV 文件名

parse_vocabulary_file(input_filename, output_filename)