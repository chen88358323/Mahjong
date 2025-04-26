import os
import hashlib
import shutil
# 将文件以及文件夹hash分片 16片
def create_subfolders(basepath, num_folders=16):
    """在basepath下创建_1到_num_folders的子文件夹"""
    for i in range(1, num_folders + 1):
        folder_path = os.path.join(basepath, f'_{i}')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


def calculate_hash(name):
    """计算给定名称的哈希值"""
    hasher = hashlib.md5()
    hasher.update(name.encode('utf-8'))
    return hasher.hexdigest()


def move_files_and_folders(basepath, num_folders=16):
    """移动basepath下的文件和文件夹到对应的子文件夹中"""
    # 获取basepath下的所有文件和文件夹
    items = os.listdir(basepath)

    # 遍历所有项目和文件夹
    for item in items:
        # 跳过_1到_16的文件夹
        if item.startswith('_') and item[1:].isdigit() and 1 <= int(item[1:]) <= num_folders:
            continue

        # 计算哈希值
        hash_value = calculate_hash(item)

        # 确定目标文件夹
        target_folder_index = int(hash_value, 16) % num_folders + 1
        target_folder = os.path.join(basepath, f'_{target_folder_index}')

        # 获取完整的源路径
        source_path = os.path.join(basepath, item)

        # 移动文件或文件夹
        if os.path.isdir(source_path):
            # 如果是文件夹，使用shutil.move移动整个文件夹
            shutil.move(source_path, os.path.join(target_folder, item))
        else:
            # 如果是文件，直接移动
            shutil.move(source_path, os.path.join(target_folder, item))


def main(basepath):
    num_folders = 16
    create_subfolders(basepath, num_folders)
    move_files_and_folders(basepath, num_folders)


if __name__ == "__main__":
    basepath = r"D:\base"
    main(basepath)
