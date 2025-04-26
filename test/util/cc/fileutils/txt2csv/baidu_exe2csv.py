import pandas as pd

file ='xxx'
# 初始化空列表来存储解析后的数据
data = []

# 当前正在处理的单词信息
current_word = {}

# 逐行解析单词本内容
for line in wordbook_file:
    line = line.strip()
    if not line:  # 如果行是空的，则跳过
        if current_word:  # 如果之前有单词信息，则添加到列表中并重置
            data.append(current_word)
            current_word = {}
    else:
        parts = line.split('/')
        if len(parts) == 1:  # 没有音标，可能是词性或定义
            if 'meaning' not in current_word:
                current_word['meaning'] = []
            current_word['meaning'].append(parts.strip())
        elif len(parts) == 2:  # 有音标和单词或定义
            word_or_pronunciation = parts.strip()
            pronunciation_or_meaning = parts.strip()
            if not current_word:  # 如果是第一个单词，则先设置单词
                current_word['word'] = word_or_pronunciation
            else:  # 否则设置音标
                current_word['pronunciation'] = pronunciation_or_meaning
                # 如果之前还没有设置meaning，则初始化一个空列表
                if 'meaning' not in current_word:
                    current_word['meaning'] = []

# 最后一个单词可能在文件末尾没有空行分隔，所以需要手动添加
if current_word:
    data.append(current_word)

# 将数据转换为DataFrame
df = pd.DataFrame(data)

# 由于可能存在多个意义，将meaning列转换为字符串（用逗号分隔）
df['meaning'] = df['meaning'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

# 重置索引，因为可能在解析过程中跳
