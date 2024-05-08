'''
这段代码作用是删除超过界限的点
'''
import os
import pandas as pd

# 定义原始文件夹路径和目标文件夹路径
original_folder_path = r'D:\Project\Convert_Dataset\轨迹预测数据\0507数据\2_original'
target_folder_path = r'D:\Project\Convert_Dataset\轨迹预测数据\0507数据\filter_0507'

# 确保目标文件夹存在
os.makedirs(target_folder_path, exist_ok=True)

# 遍历原始文件夹中的所有.csv文件
for file_name in os.listdir(original_folder_path):
    if file_name.endswith('.csv'):
        # 构造原始文件的完整路径
        original_file_path = os.path.join(original_folder_path, file_name)

        # 读取CSV文件
        df = pd.read_csv(original_file_path)

        # 假设CSV文件中有以下列名'LON'包含经度数据
        # 筛选出经度在89.5034和89.5269之间的数据
        df_filtered = df[(df['LON'] >= 89.5034) & (df['LON'] <= 89.527)]

        # 构造目标文件的完整路径
        target_file_path = os.path.join(target_folder_path, file_name)

        # 将筛选后的数据保存为新的CSV文件
        df_filtered.to_csv(target_file_path, index=False)

        print(f'文件 {file_name} 已处理，结果保存为 {target_file_path}')

print("所有文件处理完成。")