import fitz  # PyMuPDF
import os


def pdf_to_images(pdf_path, output_folder, dpi=300):
    """
    将PDF每页转换为图片
    :param pdf_path: PDF文件路径
    :param output_folder: 输出图片文件夹
    :param dpi: 输出分辨率（默认300dpi）
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        zoom = dpi / 72  # 72是PDF默认DPI
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        output_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(output_path)
    print(f"转换完成，共 {len(doc)} 页")


# 使用示例
pdf_to_images("t.pdf", "output_images")
