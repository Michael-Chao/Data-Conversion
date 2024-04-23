import os
import numpy as np

# 文件夹路径
folder_path = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\lstm_adsb_data'

# 起飞和降落的索引
takeoff = [0, 2, 4, 10, 12, 14, 16, 20, 23]
landing = [1, 3, 5, 6, 7, 8, 9, 11, 13, 15, 17, 18, 19, 21, 22, 24, 25, 26, 27, 28, 29]

# 创建目标文件夹
output_folder = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\train'
os.makedirs(output_folder, exist_ok=True)

# 创建起飞和降落的子文件夹
for subfolder in ['0', '1']:
    subfolder_path = os.path.join(output_folder, subfolder)
    os.makedirs(subfolder_path, exist_ok=True)

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

# 将合并后的数据拆分并按顺序保存为单独的.npy文件到对应的起飞或降落文件夹
for index, sample in enumerate(all_data):
    subfolder = '0' if index in takeoff else '1'
    sample_path = os.path.join(output_folder, subfolder, f"{index}.npy")
    np.save(sample_path, sample)
    print(f"Saved sample {index} to {sample_path}")

# 打印保存信息
print("所有样本已拆分并按顺序保存至：", output_folder)

# 将合并后的数据拆分并按顺序保存为单独的.npy文件到对应的起飞或降落文件夹
takeoff_count = 0
landing_count = 0
for index, sample in enumerate(all_data):
    subfolder = '0' if index in takeoff else '1'
    sample_path = os.path.join(output_folder, subfolder, f"{index}.npy")
    np.save(sample_path, sample)
    print(f"Saved sample {index} to {sample_path}")

    # 更新对应文件夹的数据计数
    if subfolder == '0':
        takeoff_count += 1
    else:
        landing_count += 1

# 打印每个文件夹的数据数量
print(f"起飞文件夹 '0' 里有 {takeoff_count} 个数据文件。")
print(f"降落文件夹 '1' 里有 {landing_count} 个数据文件。")

# 计算总的数据文件数量
total_count = takeoff_count + landing_count
print(f"合起来共有 {total_count} 个数据文件保存至：{output_folder}")