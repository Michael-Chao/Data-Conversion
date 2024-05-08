import os
import json
import pandas as pd

# 定义文件夹路径
result_adsb_folder_path = r'/轨迹预测数据/result_ADSB'
filter_adsb_folder_path = r'D:\Project\Convert_Dataset\轨迹预测数据\filter_ADSB'
output_folder = r'D:\Project\Convert_Dataset\轨迹预测数据\filter_ADSB_2'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 读取result_ADSB文件夹中的数据
result_adsb_file_path = os.path.join(result_adsb_folder_path, '20220729.txt')
with open(result_adsb_file_path, 'r') as f:
    result_adsb_lines = f.readlines()

# 将每一行转换成字典，并按TRP时间戳排序
result_adsb_data = [dict(kv.split("=") for kv in line.strip('{}').split(', ')) for line in result_adsb_lines]
result_adsb_data.sort(key=lambda x: float(x['TRP']))

# 遍历filter_ADSB文件夹中的所有文件
for file_name in os.listdir(filter_adsb_folder_path):
    if file_name.startswith('20220729') and file_name.endswith('.txt'):
        # 构造完整的文件路径
        filter_adsb_file_path = os.path.join(filter_adsb_folder_path, file_name)

        # 读取filter_ADSB文件中的数据
        with open(filter_adsb_file_path, 'r') as f:
            filter_adsb_data = json.load(f)

        # 对每个filter_ADSB数据项补充"GS"和"TA"
        for item in filter_adsb_data:
            # 找到与当前filter_ADSB数据项时间戳相近的result_ADSB数据项
            low_index, high_index = 0, len(result_adsb_data) - 1
            while low_index <= high_index:
                mid_index = (low_index + high_index) // 2
                if float(result_adsb_data[mid_index]['TRP']) == float(item['TRP']):
                    # 如果TRP完全相等
                    matched_result = result_adsb_data[mid_index]
                    break
                elif float(result_adsb_data[mid_index]['TRP']) < float(item['TRP']):
                    low_index = mid_index + 1
                else:
                    high_index = mid_index - 1

            if 'matched_result' in locals():
                if item['ADDR'] == matched_result['ADDR']:
                    item['GS'] = float(matched_result.get("GS", 0))
                    item['TA'] = float(matched_result.get("TA", 0))

        # 写入更新后的数据到新文件夹
        output_file_path = os.path.join(output_folder, file_name)
        with open(output_file_path, 'w') as f:
            json.dump(filter_adsb_data, f, indent=2)  # 使用indent美化输出格式

        print(f"Filtered data saved successfully at: {output_file_path}")