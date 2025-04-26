# -*- coding: utf-8 -*-
import pdfplumber
import fitz  # PyMuPDF
# 打开PDF文件
def read_pdf2txt_plumber(pdfpath):
    # 打开PDF文件
    with pdfplumber.open(pdfpath) as pdf:
        # 遍历PDF的每一页
        for page in pdf.pages:
            # 提取当前页的全部文本
            print(page.extract_text())
def read_pdf2txt_mupdf(pdfpath):
    with fitz.open(pdfpath) as doc:
        for page in doc:
            print('************************************'+str(page)+'*********************************')
            text = page.get_text()
            print(text)

if __name__=='__main__':
    path=r'D:\DOC\雅思\雅思彩色词汇表\彩色词汇表\list1_10 new.pdf'
    # read_pdf2txt_plumber(path)
    print("**********************")
    read_pdf2txt_mupdf(path)