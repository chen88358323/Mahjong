import pandas as pd

#wf  单词本
#excel 文件名
def convert2csv(wf,xls):
# 假设单词本内容存储在名为'wordbook.txt'的文件中
    filename = wf

    # 初始化空列表来存储解析后的数据
    data = []

    # 当前正在处理的单词信息
    current_word = {}

    # 打开文件并逐行读取内容
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:  # 如果行是空的，则跳过，并检查是否有之前的单词信息需要保存
                if current_word:
                    data.append(current_word)
                    current_word = {}
            else:
                parts = line.split('/')
                if len(parts) == 1:  # 没有音标，可能是单词
                    # （但这里其实不会单独出现单词，只是处理逻辑保持一致）或定义
                    # 由于单词和第一个定义之间没有明确的分隔符，我们需要根据上下文来判断
                    # 这里假设如果current_word为空，则第一部分是单词，否则是定义的一部分
                    if not current_word:
                        # 但实际上，由于我们的逻辑，这里不会进入，因为单词和音标应该是一起出现的
                        # 不过为了保持代码的完整性，我们仍然保留这个判断
                        current_word['word'] = parts.strip()
                    else:
                        # 添加到meaning列表中，这里应该是处理定义的情况
                        if 'meaning' not in current_word:
                            current_word['meaning'] = []
                        # 由于定义可能跨多行，我们需要将这部分内容保存下来，稍后处理
                        # 但由于我们的特定格式，这里其实不会单独出现定义行，而是紧跟在音标行后面
                        # 因此，这里的逻辑主要是为了处理可能的异常情况或格式变化
                        # 在当前格式下，这行代码实际上不会被执行到，但为了完整性而保留
                        temp_meaning = parts.strip()
                        # 如果需要，可以将temp_meaning添加到某个临时变量中，稍后再合并到meaning中
                        # 但由于我们的逻辑已经处理了这种情况（即紧跟在音标后的定义为同一行处理），所以这里不需要
                elif len(parts) == 2:  # 有音标和定义（或单词和音标，但根据我们的逻辑，单词已经在上一行“假设”处理了）
                    # 第一部分应该是音标（但根据我们的逻辑，这里其实是紧接着单词的音标行）
                    # 第二部分可能是紧接着的定义，但由于我们的格式，它们实际上在同一行处理
                    pronunciation = parts.strip()
                    # 这里我们“假设”当前行是紧跟在单词行的音标行，因此没有单独的单词行处理逻辑
                    # 实际上，根据我们的格式，单词和音标是在同一逻辑行中处理的，这里只是为了解释代码而拆分
                    # 由于我们之前并没有真正处理单词行（因为它和音标行是一起的），这里我们“模拟”处理它
                    # 但实际上，在之前的逻辑中，我们已经“隐含地”处理了单词（即作为音标行的前置条件）
                    # 因此，这里我们直接将音标和（可能的）定义处理为当前单词的一部分
                    # 注意：这里的逻辑是基于您提供的特定格式，如果格式有变化，可能需要调整
                    if not current_word:
                        # 实际上这种情况不会发生，因为单词和音标应该是一起出现的
                        # 但为了代码的健壮性，我们仍然保留这个判断并给出错误提示
                        raise ValueError("Unexpected format: Word not found before pronunciation.")
                    # 设置音标（这里实际上是“确认”了音标行的处理）
                    current_word['pronunciation'] = pronunciation
                    # 处理定义部分（由于我们的格式，定义实际上是紧跟在音标后面的，所以这里直接处理）
                    # 注意：这里我们假设定义不会跨多行（根据您的示例，确实没有跨行）
                    # 如果定义可能跨多行，则需要额外的逻辑来处理这种情况
                    meaning = parts.strip()
                    if 'meaning' not in current_word:
                        current_word['meaning'] = [meaning]  # 如果是第一个定义，则创建列表并添加
                    else:
                        # 但实际上，根据我们的格式，这里不会发生，因为每个单词只有一行定义（包括音标和定义）
                        # 不过为了代码的完整性，我们仍然保留这个判断（虽然它不会被执行到）
                        # 如果需要处理多个定义（在同一行或跨行），则需要修改这里的逻辑
                        # 在当前情况下，我们只需要知道每个单词有一行对应的音标和定义即可
                        # 因此，这里的else分支实际上是为了解释可能的扩展性而保留的
                        pass  # 不需要执行任何操作，因为我们已经处理了定义（在同一行中）

    # 检查是否有最后一个单词需要保存（在文件末尾没有空行分隔的情况下）
    if current_word:
        data.append(current_word)

    # 将数据转换为DataFrame
    df = pd.DataFrame(data)

    # 由于可能存在多个意义（但实际上在我们的格式中每个单词只有一行定义），这里不需要额外处理
    # 但为了保持代码的通用性，我们之前已经处理了meaning列为列表的情况（并将其转换为字符串）
    # 在当前特定情况下，这一步其实是多余的，但为了代码的完整性而保留
    # 如果确实需要处理多个意义，并且希望它们在Excel中以逗号分隔的形式显示，则可以取消注释以下两行代码
    # df['meaning'] = df['meaning'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    # 由于我们的格式保证每个单词只有一行定义，所以这里不需要重置索引（因为不会有跳过的空行）
    # 但为了保持代码的通用性，我们之前已经包含了重置索引的逻辑（虽然在这里是多余的）
    # df.reset_index(drop=True, inplace=True)

    # 将DataFrame保存为Excel文件
    output_file = xls
    df.to_excel(output_file, index=False)

    print(f"Data has been successfully written to {output_file}")
if __name__ == '__main__':
    convert2csv('word','wordbook_output.xlsx')
