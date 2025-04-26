import os
import shutil
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 用于存储去重后的资源路径
unique_resources = set()
html_directory = r'D:\CODE\cms\mcms-cc\src\main\webapp\html\web'
base_resource_dir = r'D:\CODE\cms\mcms-cc\src\main\webapp'
clone_dir = r'D:\temp\clone'
def find_html_files(html_directory):
    """递归地找到给定目录中的所有 HTML 文件。"""
    html_files = []
    for root, dirs, files in os.walk(html_directory):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

def extract_resources(html_file, base_resource_dir):
    """解析 HTML 文件，提取资源路径，并转换为绝对路径。"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    resources = []
    for tag in soup.find_all(['script', 'img', 'link']):  # 也可以添加其他需要提取的标签，如link（用于CSS）
        src = tag.get('src') or tag.get('href')  # 对于link标签使用href属性
        if src:
            unique_resources.add(src.strip())

    # 将style="background:url(/xxx.jpeg) 此类css样式的静态资源进行提取
    css_background_images = set()
    for style in soup.find_all('style'):
        if style.string:
            background_images = re.findall(r'background\s*:\s*url\s*\(\s*[\'"]?(.*?)[\'"]?\s*\)\s*;', style.string)
            css_background_images.update(background_images)

    for tag in soup.find_all(style=True):
        style_content = tag.get('style')
        background_images = re.findall(r'background\s*:\s*url\s*\(\s*[\'"]?(.*?)[\'"]?\s*\)\s*;', style_content)
        css_background_images.update(background_images)

    # 将提取到的CSS背景图片链接加入到unique_resources中
    for image in css_background_images:
        unique_resources.add(image)

    #复制html到clone目录
    new_html_file=clone_dir+html_file.replace(base_resource_dir,'');
    # 确保目标目录存在
    os.makedirs(os.path.dirname(new_html_file), exist_ok=True)
    shutil.copyfile(html_file,new_html_file)

#将style="background:url(/xxx.jpeg) 此类css样式的静态资源进行提取
def find_css_resources(html_content):
    """
    使用正则表达式从HTML内容中提取CSS样式引用的静态资源链接
    """
    pattern = re.compile(r'style="["]*url\(([)]+)\)["]*"')
    matches = pattern.findall(html_content)
    resources = {match.strip() for match in matches if match.strip()}
    return resources
# 将静态页面链接转换为win路径
def convert2_win_abspath(url):
    url=url.strip()
    if url is not None:
        if (not url.startswith("http")):
            # 转换为win路径链接
            url = url.strip().replace('/', '\\')
        unique_resources.add(url)
def copy_resources_to_clone_dir(clone_dir, base_resource_dir):
    """将去重后的资源复制到克隆目录下，保持目录结构。"""
    for resource_path in unique_resources:
        if(resource_path.startswith("http")):
            print('==>'+resource_path)
        else:
            #源文件
            source_file=base_resource_dir + resource_path
            target_file=clone_dir+resource_path
            # 确保目标目录存在
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            # 复制文件
            shutil.copy2(source_file, target_file)


def main():
    # html_directory = r'D:\CODE\html'
    # base_resource_dir = r'D:\CODE'
    # clone_dir = r'D:\temp\clone'



    # 确保克隆目录存在
    os.makedirs(clone_dir, exist_ok=True)

    # 找到所有 HTML 文件
    html_files = find_html_files(html_directory)

    # 提取资源路径
    for html_file in html_files:
        extract_resources(html_file, base_resource_dir)

        # 统一打印去重后的资源
    for resource in unique_resources:
        print(resource)

    # 复制资源到克隆目录
    copy_resources_to_clone_dir(clone_dir, base_resource_dir)

if __name__ == "__main__":
    main()
