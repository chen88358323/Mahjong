import os
from bs4 import BeautifulSoup
import shutil
import re

# HTML文件路径
html_file_path = 'path/to/your/htmlfile.html'
# 资源文件夹路径
resources_dir = 'path/to/your/resources'
# 未使用资源的目标文件夹
undone_dir = 'path/to/your/undone'

# 确保undone文件夹存在
os.makedirs(undone_dir, exist_ok=True)

# 读取HTML文件
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')

# 提取所有静态资源的URL
# 这里我们只考虑<img>, <script>, 和 <link rel="stylesheet">
used_resources = set()
for img in soup.find_all('img'):
    used_resources.add(img['src'])
for script in soup.find_all('script'):
    if script.get('src'):
        used_resources.add(script['src'])
for link in soup.find_all('link'):
    if link.get('rel') == ['stylesheet'] and link.get('href'):
        used_resources.add(link['href'])

# 修正资源路径，使其相对于resources_dir
used_resources = {os.path.join(resources_dir, re.sub(r'/', '', url)) for url in used_resources}

# 列出所有资源文件
all_resources = {os.path.join(resources_dir, f) for f in os.listdir(resources_dir)}

# 找出未使用的资源
unused_resources = all_resources - used_resources

# 移动未使用的资源
for resource_path in unused_resources:
    target_path = os.path.join(undone_dir, os.path.basename(resource_path))
    shutil.move(resource_path, target_path)
    print(f'Moved {resource_path} to {target_path}')

print("Done.")
