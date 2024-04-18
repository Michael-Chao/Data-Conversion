import os
import numpy as np

# 文件夹路径
folder_path = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\lstm_adsb_data'

# 创建一个空列表，用于存储所有.npy文件的数据
all_data = []

# 遍历文件夹
for subdir in os.listdir(folder_path):
    subdir_path = os.path.join(folder_path, subdir)
    # 如果是文件夹
    if os.path.isdir(subdir_path):
        for file in os.listdir(subdir_path):
            # 如果文件是.npy文件
            if file.endswith('.npy'):
                file_path = os.path.join(subdir_path, file)
                # 加载.npy文件的数据
                data = np.load(file_path)
                # 打印数据的形状
                print("Loaded data shape from", file_path, ":", data.shape)
                # 将数据添加到列表中
                all_data.append(data)

# 将列表中的数据合并为一个大的NumPy数组
all_data = np.concatenate(all_data, axis=0)

# 打印合并后的数据的形状
print("合并后的数据形状：", all_data.shape)

# 保存合并后的数据为一个新的.npy文件
output_path = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\train\1.npy'
np.save(output_path, all_data)

# 打印保存信息
print("合并后的数据已保存至：", output_path)
