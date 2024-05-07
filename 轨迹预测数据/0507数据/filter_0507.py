import os
import json
import pandas as pd

# 定义原始数据文件夹和目标数据文件夹的路径
原始文件夹路径 = r'D:\Project\Convert_Dataset\轨迹预测数据\filter_ADSB_0506'
目标文件夹路径 = r'D:\Project\Convert_Dataset\轨迹预测数据\filter_0507'

# 确保目标文件夹存在
os.makedirs(目标文件夹路径, exist_ok=True)

# 遍历原始文件夹中的所有.txt文件
for 文件名 in os.listdir(原始文件夹路径):
    if 文件名.endswith('.txt'):
        # 构造完整的文件路径
        原始文件路径 = os.path.join(原始文件夹路径, 文件名)

        # 读取JSON数据
        with open(原始文件路径, 'r') as f:
            数据 = json.load(f)

        # 提取所需的字段
        df = pd.DataFrame([item for item in 数据 if 'LON' in item and 'LAT' in item and 'TA' in item and 'GS' in item],
                          columns=['TRP', 'LON', 'LAT', 'TA', 'GS'])

        # 将提取的数据保存为.csv文件
        目标文件名 = os.path.splitext(文件名)[0] + '.csv'  # 将.txt后缀改为.csv
        目标文件路径 = os.path.join(目标文件夹路径, 目标文件名)
        df.to_csv(目标文件路径, index=False)

        print(f'文件 {文件名} 已处理，结果保存为 {目标文件名}')

print("所有文件处理完成。")