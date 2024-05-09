import os
import pandas as pd

# 原始文件夹路径
input_folder = r'D:\Project\Convert_Dataset\轨迹预测数据\0509数据\起飞\1_original_0508'

# 输出文件夹路径
output_folder = r'D:\Project\Convert_Dataset\轨迹预测数据\0509数据\起飞\2_deduplication_0508'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 处理每个文件
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        # 读取CSV文件
        input_file_path = os.path.join(input_folder, filename)
        data = pd.read_csv(input_file_path)

        # 找到相邻经度和纬度重复的点，并替换为平均值
        prev_lon = None
        prev_lat = None
        prev_ta = None
        prev_gs = None
        prev_trp = None
        prev_index = None
        rows_to_drop = []
        for index, row in data.iterrows():
            if prev_lon is not None and prev_lon == row['LON'] and abs(prev_trp - row['TRP']) < 1:
                # 计算平均值
                avg_lon = (prev_lon + row['LON']) / 2
                avg_lat = (prev_lat + row['LAT']) / 2
                avg_ta = (prev_ta + row['TA']) / 2
                avg_gs = (prev_gs + row['GS']) / 2
                avg_trp = (prev_trp + row['TRP']) / 2

                # 用平均值替代
                data.at[prev_index, 'LON'] = avg_lon
                data.at[prev_index, 'LAT'] = avg_lat
                data.at[prev_index, 'TA'] = avg_ta
                data.at[prev_index, 'GS'] = avg_gs
                data.at[prev_index, 'TRP'] = avg_trp

                # 标记需要删除的行
                rows_to_drop.append(index)

            # 更新上一个点的信息
            prev_lon = row['LON']
            prev_lat = row['LAT']
            prev_ta = row['TA']
            prev_gs = row['GS']
            prev_trp = row['TRP']
            prev_index = index

        # 删除经度重复的行
        data.drop(rows_to_drop, inplace=True)

        # 重新初始化变量，用于处理纬度重复的点
        prev_lon = None
        prev_lat = None
        prev_ta = None
        prev_gs = None
        prev_trp = None
        prev_index = None
        rows_to_drop = []
        for index, row in data.iterrows():
            if prev_lat is not None and prev_lat == row['LAT'] and abs(prev_trp - row['TRP']) < 1:
                # 计算平均值
                avg_lon = (prev_lon + row['LON']) / 2
                avg_lat = (prev_lat + row['LAT']) / 2
                avg_ta = (prev_ta + row['TA']) / 2
                avg_gs = (prev_gs + row['GS']) / 2
                avg_trp = (prev_trp + row['TRP']) / 2

                # 用平均值替代
                data.at[prev_index, 'LON'] = avg_lon
                data.at[prev_index, 'LAT'] = avg_lat
                data.at[prev_index, 'TA'] = avg_ta
                data.at[prev_index, 'GS'] = avg_gs
                data.at[prev_index, 'TRP'] = avg_trp

                # 标记需要删除的行
                rows_to_drop.append(index)

            # 更新上一个点的信息
            prev_lon = row['LON']
            prev_lat = row['LAT']
            prev_ta = row['TA']
            prev_gs = row['GS']
            prev_trp = row['TRP']
            prev_index = index

        # 删除纬度重复的行
        data.drop(rows_to_drop, inplace=True)

        # 保存处理后的数据到CSV文件
        output_file_path = os.path.join(output_folder, filename)
        data.to_csv(output_file_path, index=False)

        print("处理完成，结果已保存到", output_file_path)
