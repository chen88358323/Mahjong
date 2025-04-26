import PyPDF2


def merge_pdfs(paths, output):
    pdf_writer = PyPDF2.PdfWriter()

    for path in paths:
        pdf_reader = PyPDF2.PdfReader(path)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

    with open(output, 'wb') as out:
        pdf_writer.write(out)


paths = [r'D:\DOC\person\华为云身份变更\华为云身份认证变更\1.pdf', r'D:\DOC\person\华为云身份变更\华为云身份认证变更\2.pdf']  # 要合并的PDF文件列表
output = r'D:\DOC\person\华为云身份变更\华为云身份认证变更\merged.pdf'  # 合并后的PDF文件名
merge_pdfs(paths, output)