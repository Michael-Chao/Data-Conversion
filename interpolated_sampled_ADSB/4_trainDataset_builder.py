import os
import numpy as np

# 定义输入和输出路径
input_dir = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\lstm_adsb_data'
train_dir = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\train'

# 定义起飞和降落文件夹索引
takeoff = [0, 2, 4, 10, 12, 14, 16, 20, 23]
landing = [1, 3, 5, 6, 7, 8, 9, 11, 13, 15, 17, 18, 19, 21, 22, 24, 25, 26, 27, 28, 29]

# 定义adsb_contents列表
adsb_contents = ['20220701_1', '20220701_2', '20220701_3', '20220701_4',
                 '20220703_1', '20220703_2', '20220703_4',
                 '20220704_1', '20220704_2', '20220704_3', '20220704_4',
                 '20220706_1', '20220706_2', '20220706_3', '20220706_4',
                 '20220708_1', '20220708_2', '20220708_4',
                 '20220710_1', '20220710_2', '20220710_4',
                 '20220711_1', '20220711_2', '20220711_4',
                 '20220713_2',
                 '20220715_2',
                 '20220718_4',
                 '20220719_2',
                 '20220720_2',
                 '20220724_4']

# 确保训练文件夹存在
os.makedirs(train_dir, exist_ok=True)
os.makedirs(os.path.join(train_dir, '0'), exist_ok=True)
os.makedirs(os.path.join(train_dir, '1'), exist_ok=True)

# 初始化计数器
total_count = 0

# 遍历adsb_contents中的每个文件夹
for folder_name in adsb_contents:
    print(f"正在处理文件夹：{folder_name}")  # 打印正在处理的文件夹信息

    # 确定.npy文件应该保存到哪个子文件夹（起飞或降落）
    index = adsb_contents.index(folder_name)
    target_folder = '0' if index in takeoff else '1'
    target_path = os.path.join(train_dir, target_folder)

    # 遍历文件夹中的所有.npy文件
    input_folder_path = os.path.join(input_dir, folder_name)
    for file_name in os.listdir(input_folder_path):
        if file_name.endswith('.npy'):
            file_path = os.path.join(input_folder_path, file_name)
            data = np.load(file_path)  # 加载.npy文件数据

            # 根据数据的形状拆分.npy文件
            num_samples = data.shape[0]
            for i in range(num_samples):
                sample = data[i, ...]
                output_file_path = os.path.join(target_path, f"{total_count}.npy")  # 保存到目标文件夹，文件名从0开始递增
                np.save(output_file_path, sample)  # 保存样本

                total_count += 1
                print(f"保存文件 {total_count}.npy 到 {output_file_path}")

# 打印统计信息
# 重新读取文件夹，获取实际的.npy文件数量
actual_count_0 = len(os.listdir(os.path.join(train_dir, '0')))
actual_count_1 = len(os.listdir(os.path.join(train_dir, '1')))

# 打印实际的.npy文件数量
print(f"起飞文件夹 '0' 里有 {actual_count_0} 个.npy文件。")
print(f"降落文件夹 '1' 里有 {actual_count_1} 个.npy文件。")
