import pandas as pd
import dataframe_image as dfi

def export_excel_to_image(excel_filepath, image_filepath, sheet_name=0):
    """
    将 Excel 文件中的指定工作表导出为图片，空白格填充为空字符串。

    Args:
        excel_filepath (str): Excel 文件的路径。
        image_filepath (str): 保存图片的路径。
        sheet_name (int or str): 要导出的工作表名称或索引（默认为第一个工作表）。
    """
    try:
        df = pd.read_excel(excel_filepath, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"错误：文件 {excel_filepath} 未找到。")
        return
    except Exception as e:
        print(f"读取 Excel 文件时发生错误：{e}")
        return

    if df.empty:
        print("错误：Excel 文件中没有数据。")
        return

    # 将 NaN 填充为空字符串
    df = df.fillna('')
    # 定义 CSS 样式
    css_styles = [
        {'selector': '.col_日期', 'props': [('text-align', 'center'),('width', '100px')]},  # 设置固定宽度为 80 像素)]},
        {'selector': '.col_地点', 'props': [('text-align', 'left')]},
        {'selector': '.col_证据', 'props': [('text-align', 'left')]},
        {'selector': '.col_备注', 'props': [('text-align', 'left')]}
    ]

    try:
        dfi.export(df, image_filepath)#, table_conversion='matplotlib', table_css=css_styles
        print(f"成功将 Excel 工作表 '{sheet_name}' 导出为图片：{image_filepath}")
    except ImportError:
        print("错误：需要安装 'dataframe_image' 库。请运行 'pip install dataframe_image'")
    except Exception as e:
        print(f"导出 DataFrame 为图片时发生错误：{e}")

if __name__ == "__main__":
    excel_file = "wg.xls"  # 将 'your_table_data.xlsx' 替换为你的 Excel 文件名
    image_file = "table_image.png"  # 你想要保存的图片文件名

    # 确保你的 Excel 文件 'your_table_data.xlsx' 存在，并且包含你想要导出的表格数据。
    # 你可以使用 pandas 创建一个简单的 Excel 文件进行测试：
    #
    # data = {'日期': ['2023-12-29', '2023-12-29', '2023-12-30', '2024-01-02', '2024-01-03'],
    #         '地点': ['案发地点', '天津医科大学第二附属医院', '友谊路派出所', '天津医科大学第二附属医院', '天津市第一中心医院(水西园区)'],
    #         '证据': ['', '当日发票一审已提交', '当日询问笔录已提交', '支付宝支付截图 (2024年1月2日)', '当日发票一审已提交'],
    #         '备注': ['事发当天，后前往天津医科大学第二附属医院', '急救', '上午去友谊路派出所做笔录，下午去医院急诊就诊', '由于事发在元旦假日，假日期间，二附属医院无法进行耳镜拍摄，顾在工作日时间进行挂号及耳镜拍摄，但当天被告知拍摄耳镜机器故障，故去友谊路派出所重新开取伤单，指定天津市第一中心医院(水西园区)为就诊医院', '就医，除听力外诊断进行就医，听力诊断需预约，后择期就诊']}
    # df_test = pd.DataFrame(data)
    # df_test.to_excel(excel_file, index=False)

    export_excel_to_image(excel_file, image_file)