from PIL import Image
import os
from PyPDF2 import PdfMerger
def convert_imgs_21pdf(directory):
    # 列出目录中的所有文件
    files = os.listdir(directory)

    # 筛选出jpg格式的文件，并确保它们按文件名排序
    jpg_files = sorted([f for f in files if f.endswith('.jpg') and f.startswith('000')])

    # 打印排序后的文件名列表
    print("排序后的文件名：")
    for jpg in jpg_files:
        print(jpg)

    # 检查是否存在jpg文件
    if not jpg_files:
        print("未找到任何jpg文件。")
        return

    # 设置PDF文件的输出路径
    output_pdf_path = os.path.join(directory, 'output.pdf')

    # 打开第一张图片，并初始化PDF文件
    first_img = Image.open(os.path.join(directory, jpg_files[0]))
    first_img.save(output_pdf_path, 'PDF', save_all=False)
    # 这里设置为False，因为我们将在循环中追加图片

    # 创建一个Image对象列表，用于保存所有要添加到PDF中的图片
    images = [first_img]

    # 将剩余的图片追加到图片列表中
    for jpg in jpg_files[1:]:
        img_path = os.path.join(directory, jpg)
        img = Image.open(img_path)
        images.append(img)

    # 使用Image.save()方法将所有图片保存为PDF
    images.save(output_pdf_path, 'PDF', save_all=True, append_images=images[1:])

    print(f"PDF文件已成功保存至：{output_pdf_path}")
def convert_imgs_21pdf_v2(directory):
    # 获取目录中所有jpg格式的文件，并按照文件名进行排序
    jpg_files = sorted([f for f in os.listdir(directory) if f.endswith('.jpg')])

    # 检查是否有图片文件
    if not jpg_files:
        print("没有找到jpg图片文件。")
        return

    # 打印排序后的文件名
    for jpg in jpg_files:
        print(jpg)

    # 打开第一张图片，并将其保存为PDF的起始页
    output_pdf_path = os.path.join(directory,'output.pdf')
    first_img_path = os.path.join(directory, jpg_files[0])
    first_img = Image.open(first_img_path)
    first_img.save(output_pdf_path, 'PDF', save_all=True)

    # 迭代剩余的图片，并将它们追加到PDF中
    for jpg in jpg_files[1:]:
        img_path = os.path.join(directory, jpg)
        img = Image.open(img_path)
        first_img.save(output_pdf_path, 'PDF', save_all=True, append_images=[img])

    print(f"PDF文件已保存至：{output_pdf_path}")





def convert_imgs_to_pdfs(directory):
    # 列出目录中的所有文件
    files = os.listdir(directory)

    # 筛选出jpg格式的文件，并确保它们按文件名排序
    jpg_files = sorted([f for f in files if f.endswith('.jpg') and f.startswith('000')])

    # 打印排序后的文件名列表
    print("排序后的文件名：")
    for jpg in jpg_files:
        print(jpg)

    # 检查是否存在jpg文件
    if not jpg_files:
        print("未找到任何jpg文件。")
        return

    # 用于存储单独PDF文件的路径列表
    pdf_files = []

    # 将每张图片转换为单独的PDF文件
    for jpg in jpg_files:
        img_path = os.path.join(directory, jpg)
        img = Image.open(img_path)
        pdf_path = os.path.join(directory, f"{os.path.splitext(jpg)}.pdf")
        img.save(pdf_path, 'PDF')
        pdf_files.append(pdf_path)

    # 合并所有单独的PDF文件为一个PDF文件
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)

    output_pdf_path = os.path.join(directory, 'meoutput.pdf')
    merger.write(output_pdf_path)
    merger.close()

    # 打印合并后的PDF文件路径
    print(f"合并后的PDF文件已成功保存至：{output_pdf_path}")


#可用
def convert_imgs_to_single_pdf(directory):
    # 列出目录中的所有文件
    files = os.listdir(directory)

    # 筛选出jpg格式的文件，并确保它们按文件名排序
    jpg_files = sorted([f for f in files if f.endswith('.jpg') and f.startswith('000')])

    # 打印排序后的文件名列表
    print("排序后的文件名：")
    for jpg in jpg_files:
        print(jpg)

    # 检查是否存在jpg文件
    if not jpg_files:
        print("未找到任何jpg文件。")
        return

    # 设置所有图片的统一大小
    target_size = (595, 842)  # A4纸大小，单位为像素

    # 用于存储临时PDF文件的路径列表
    pdf_files = []

    # 将每张图片调整为统一大小并转换为单独的PDF文件
    for jpg in jpg_files:
        img_path = os.path.join(directory, jpg)
        with Image.open(img_path) as img:
            # 调整图片大小
            img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
            # 设置PDF文件的路径
            pdf_path = os.path.join(directory, f"{os.path.splitext(jpg)}.pdf")
            # 保存为PDF
            img_resized.save(pdf_path, 'PDF')
            pdf_files.append(pdf_path)

    # 合并所有单独的PDF文件为一个PDF文件
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)

    output_pdf_path = os.path.join(directory, 'merged_output.pdf')
    merger.write(output_pdf_path)
    merger.close()

    # 打印合并后的PDF文件路径
    print(f"合并后的PDF文件已成功保存至：{output_pdf_path}")

    # 可选：删除临时生成的单独PDF文件
    for pdf in pdf_files:
        os.remove(pdf)



# 调用函数，并指定图片所在的目录
if __name__ == '__main__':
    convert_imgs_to_single_pdf(r'C:\Users\Administrator\Desktop\fan')
    # 将所有图片保存为一个PDF文件
    convert_imgs_to_pdfs(r'C:\Users\Administrator\Desktop\fan')
    # convert_imgs_21pdf(r'C:\Users\Administrator\Desktop\fan')





    # 调用函数，指定图片所在的目录
    # convert_imgs_21pdf(r'C:\Users\Administrator\Desktop\fan')
