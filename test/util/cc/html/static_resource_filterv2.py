import os
from bs4 import BeautifulSoup
import shutil
import re

# a文件夹路径
a_folder_path = r'D:\CODE\cms\mcms-cc\src\main\webapp\html\web'
# 资源文件夹路径（与a文件夹同级或指定路径）
resources_dir = 'path/to/your/resources'
# 未使用资源的目标文件夹
undone_dir = 'path/to/your/undone'

# 确保undone文件夹存在
os.makedirs(undone_dir, exist_ok=True)

# 遍历a文件夹中的所有HTML文件
html_files = [os.path.join(a_folder_path, f) for f in os.listdir(a_folder_path) if f.endswith('.html')]

# 用于存储所有HTML文件中引用的资源
used_resources = set()

# 解析每个HTML文件并提取资源
for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取<img>, <script>, 和 <link rel="stylesheet">中的资源
    for img in soup.find_all('img'):
        used_resources.add(os.path.join(resources_dir, img['src']))
    for script in soup.find_all('script'):
        if script.get('src'):
            used_resources.add(os.path.join(resources_dir, script['src']))
    for link in soup.find_all('link'):
        if link.get('rel') == ['stylesheet'] and link.get('href'):
            used_resources.add(os.path.join(resources_dir, link['href']))

# 列出资源文件夹中的所有文件
all_resources = {os.path.join(resources_dir, f) for f in os.listdir(resources_dir)}

# 找出未使用的资源
unused_resources = all_resources - used_resources

# 移动未使用的资源到undone文件夹
for resource_path in unused_resources:
    print(resource_path)

    # if resource_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')):  # 检查是否为图片文件
    #     target_path = os.path.join(undone_dir, os.path.basename(resource_path))
    #     shutil.move(resource_path, target_path)
    #     print(f'Moved {resource_path} to {target_path}')

print("Done.")
