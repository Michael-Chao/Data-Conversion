

import os
import numpy as np

def process_file(file_path):
    # 读取.txt文件的数据
    with open(file_path, 'r') as f:
        lines = f.readlines()
        data = [list(map(float, line.strip().split(','))) for line in lines]

    # 按每组15个数据进行采集
    grouped_data = [data[i:i + 15] for i in range(0, len(data), 15)]

    # 补充缺少的数据并填充至15个
    if len(grouped_data) > 1 and len(grouped_data[-1]) < 15:
        remaining_count = 15 - len(grouped_data[-1])
        last_group = grouped_data[-1]
        second_last_group = grouped_data[-2]
        padding_data = second_last_group[-remaining_count:]
        grouped_data[-1] = padding_data + last_group

    return grouped_data

def save_data_if_valid(grouped_data, output_folder_path, file_name):
    # 如果数据少于15个则不保存
    if any(len(group) < 15 for group in grouped_data):
        return
    # 否则保存为.npy文件
    np.save(os.path.join(output_folder_path, file_name + '.npy'), np.array(grouped_data, dtype=np.float32))

def process_folder(input_dir, output_dir):
    # 创建输出文件夹
    os.makedirs(output_dir, exist_ok=True)

    # 遍历每个文件夹
    for folder in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder)
        if os.path.isdir(folder_path):
            output_folder_path = os.path.join(output_dir, folder)
            os.makedirs(output_folder_path, exist_ok=True)

            # 遍历每个.txt文件
            for file in os.listdir(folder_path):
                if file.endswith('.txt'):
                    file_path = os.path.join(folder_path, file)
                    grouped_data = process_file(file_path)
                    save_data_if_valid(grouped_data, output_folder_path, file[:-4])

def main():
    # 输入路径和输出路径
    input_dir = 'D:/Project/Convert_Dataset/interpolated_sampled_ADSB/resampled_ADSBcut'
    output_dir = 'D:/Project/Convert_Dataset/interpolated_sampled_ADSB/lstm_adsb_data'

    # 调用函数处理文件夹
    process_folder(input_dir, output_dir)

if __name__ == "__main__":
    main()