import re
def read_utf8txt(filepath):
# 方法1：直接读取并解码（适用于文本文件）
    with open(filepath, 'rb') as file:  # 'rb' 表示二进制模式读取
        byte_data = file.read()  # 读取字节数据
        string_data = byte_data.decode('utf-8', errors='ignore')  # 解码为字符串（UTF-8）
    print(string_data)
    print("**********************************"+filepath
          +"****************************************")

    res=extract_utf8(byte_data)
    print(res)


# 尝试解码所有可识别的UTF-8序列
def extract_utf8(byte_str):
    result = []
    # 使用正则表达式匹配有效的UTF-8字节序列
    pattern = re.compile(b'([\x20-\x7E]|[\xC0-\xDF][\x80-\xBF]|[\xE0-\xEF][\x80-\xBF]{2}|[\xF0-\xF7][\x80-\xBF]{3})+')

    for match in pattern.finditer(byte_str):
        try:
            decoded = match.group(0).decode('utf-8')
            if len(decoded) > 3:  # 只保留有意义的长度
                result.append(decoded)
        except UnicodeDecodeError:
            continue

    return result


if __name__ == "__main__":
    # read_utf8txt(file)
    file = r"222\xx.torrent"
    read_utf8txt(file)
