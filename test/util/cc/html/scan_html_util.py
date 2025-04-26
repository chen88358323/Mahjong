import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# 注意：Python 3 中 sets 模块已经被废弃，我们应该使用内置的 set 类型
# 这里我假设你想要一个全局的去重集合
unique_resources = set()


def find_html_files(directory):
    """递归地找到给定目录中的所有 HTML 文件。"""
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files


def extract_resources(html_file, base_url):
    """从 HTML 文件中提取 JS 和图片资源，并添加到全局去重集合中。"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    # 提取 <script> 标签中的 src 属性
    for script in soup.find_all('script', src=True):
        # 如果是相对路径，则转换为绝对路径
        src = urljoin(base_url, script['src'])
        unique_resources.add(src)

    # 提取 <img> 标签中的 src 属性
    for img in soup.find_all('img', src=True):
        # 如果是相对路径，则转换为绝对路径
        src = urljoin(base_url, img['src'])
        unique_resources.add(src)


def main(directory):
    html_files = find_html_files(directory)

    for html_file in html_files:
        # 每个 HTML 文件的基 URL 是其目录和文件名（不带扩展名）
        base_url = os.path.dirname(html_file) + '/'
        # 如果 HTML 文件在根目录，则基 URL 应该是 '/' 或者空字符串（取决于你的环境）
        if base_url == './':
            base_url = ''  # 或者 '/'，取决于你的路径解析逻辑

        # 提取资源并去重
        extract_resources(html_file, base_url)

    # 统一打印去重后的资源
    for resource in unique_resources:
        print(resource)


if __name__ == "__main__":
    directory = r"D:\CODE\cms\mcms-cc\src\main\webapp\html\web"  # Replace with your directory path
    main(directory)

   #
   # html_directory = r'D:\CODE\cms\mcms-cc\src\main\webapp\html\web'
   #  base_resource_dir = r'D:\CODE\cms\mcms-cc\src\main\webapp'
   #  clone_dir = r'D:\temp\clone'