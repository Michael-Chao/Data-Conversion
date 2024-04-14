import json
import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font

# 基础路径
base_path = r'D:\Project\Convert_Dataset\fusiondata\filter_ADSB'
# 文件名列表
adsb_contents = ['20220701_1.txt', '20220701_2.txt', '20220701_3.txt', '20220701_4.txt',
                 '20220703_1.txt', '20220703_2.txt', '20220703_4.txt',
                 '20220704_1.txt', '20220704_2.txt', '20220704_3.txt', '20220704_4.txt',
                 '20220706_1.txt', '20220706_2.txt', '20220706_3.txt', '20220706_4.txt',
                 '20220708_1.txt', '20220708_2.txt', '20220708_4.txt',
                 '20220710_1.txt', '20220710_2.txt', '20220710_4.txt',
                 '20220711_1.txt', '20220711_2.txt', '20220711_4.txt',
                 '20220713_2.txt',
                 '20220715_2.txt',
                 '20220718_4.txt',
                 '20220719_2.txt',
                 '20220720_2.txt',
                 '20220724_4.txt']

# 指定保存Excel文件的文件夹路径
folder_path = r'D:\Project\Convert_Dataset\TRP_values'

# 确保文件夹存在，如果不存在则创建
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 遍历文件名列表
for file_name in adsb_contents:
    # 移除.txt扩展名，并添加.xlsx扩展名
    excel_file_name = os.path.splitext(file_name)[0] + '.xlsx'

    # 构建完整的文件路径
    adsb_path = os.path.join(base_path, file_name)

    # 读取文件内容
    with open(adsb_path, 'r', encoding='utf-8') as file:
        data_content = file.read()

    # 解析JSON数组
    data_array = json.loads(data_content)

    # 提取TRP值
    trp_values = [float(record['TRP']) for record in data_array]

    # 计算TRP值的差值，第一个值的差值设为0
    diff_values = [0] + [trp_values[i + 1] - trp_values[i] for i in range(len(trp_values) - 1)]

    # 创建DataFrame，包含原始TRP值和差值
    df = pd.DataFrame({'TRP': trp_values, 'TRP_Difference': diff_values})

    # 指定保存Excel文件的文件夹路径
    folder_path = r'D:\Project\Convert_Dataset\TRP_values'

    # 确保文件夹存在，如果不存在则创建
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 构建完整的Excel文件路径
    excel_file_path = os.path.join(folder_path, excel_file_name)

    # 使用ExcelWriter来保存Excel文件
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        # 获取Excel文件的Workbook对象
        workbook = writer.book

        # 创建红色字体的格式
        red_font = Font(color="FF0000")

        # 获取工作表
        worksheet = workbook['Sheet1']

        # 应用格式到差值大于3的单元格
        for row_num, value in enumerate(df['TRP_Difference'], start=2):  # 从第二行开始，因为第一行是标题
            if value > 3:
                worksheet.cell(row=row_num, column=df.columns.get_loc('TRP_Difference') + 1,
                               value=value).font = red_font

        # 保存Excel文件
        workbook.save(excel_file_path)