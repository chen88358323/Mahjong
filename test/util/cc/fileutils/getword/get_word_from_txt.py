import re

def extract_words_from_file(filename):
    """
    从指定文件中读取文本，并提取单独占据一行的英文字母单词。

    Args:
        filename (str): 要读取的文本文件名。

    Returns:
        list: 包含提取出的单词的列表。
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 '{filename}'")
        return []

    words = re.findall(r'^[a-zA-Z]+$', text, re.MULTILINE)
    return words

if __name__ == "__main__":
    input_filename = "test.txt"  # 替换为您的文件名
    extracted_words = extract_words_from_file(input_filename)
    for word in extracted_words:
        print(word)