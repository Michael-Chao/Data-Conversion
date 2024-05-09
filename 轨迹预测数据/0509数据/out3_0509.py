import os
import numpy as np

def process_file(file_path, data_points_per_group, skip_points):
    """
    读取.txt文件的数据，并按指定数量的数据进行采集，并跳过指定数量的数据点。

    参数：
    file_path: 文件路径
    data_points_per_group: 每组数据点的数量
    skip_points: 采集一组数据点后需要跳过的数据点数量

    返回：
    grouped_data: 采集并处理后的数据
    """
    # 读取.txt文件的数据
    with open(file_path, 'r') as f:
        lines = f.readlines()
        data = [list(map(float, line.strip().split(','))) for line in lines]

    # 按指定数量的数据进行采集，并跳过指定数量的点
    grouped_data = []
    i = 0
    while i + data_points_per_group <= len(data):
        grouped_data.append(data[i:i + data_points_per_group])
        i += skip_points

    # 检查最后一个分组是否小于data_points_per_group，并进行填充
    if len(grouped_data) > 1 and len(grouped_data[-1]) < data_points_per_group:
        remaining_count = data_points_per_group - len(grouped_data[-1])
        last_group = grouped_data[-1]
        second_last_group = grouped_data[-2]
        padding_data = second_last_group[-remaining_count:]
        grouped_data[-1] = padding_data + last_group

    return grouped_data


def save_data_if_valid(grouped_data, output_folder_path, file_name, data_points_per_group):
    """
    如果数据满足要求（每组数据点数量不少于指定数量），且数据不为空，则保存为.npy文件。

    参数：
    grouped_data: 待保存的数据
    output_folder_path: 输出文件夹路径
    file_name: 文件名
    data_points_per_group: 每组数据点的数量
    """
    # 如果数据为空，则不保存
    if not grouped_data:
        return

    # 如果数据少于指定数量则不保存
    if any(len(group) < data_points_per_group for group in grouped_data):
        return

    # 否则保存为.npy文件
    np.save(os.path.join(output_folder_path, file_name + '.npy'), np.array(grouped_data, dtype=np.float32))

def process_folder(input_dir, output_dir, data_points_per_group, skip_points):
    """
    处理输入文件夹中的所有文件。

    参数：
    input_dir: 输入文件夹路径
    output_dir: 输出文件夹路径
    data_points_per_group: 每组数据点的数量
    skip_points: 采集一组数据点后需要跳过的数据点数量
    """
    # 创建输出文件夹
    os.makedirs(output_dir, exist_ok=True)

    # 遍历每个文件夹
    for folder in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder)
        if os.path.isdir(folder_path):
            output_folder_path = os.path.join(output_dir, folder)
            os.makedirs(output_folder_path, exist_ok=True)

            print(f"正在处理文件夹：{folder_path}")

            # 遍历每个.txt文件
            for file in os.listdir(folder_path):
                if file.endswith('.txt'):
                    file_path = os.path.join(folder_path, file)
                    print(f"正在处理文件：{file_path}")
                    grouped_data = process_file(file_path, data_points_per_group, skip_points)
                    save_data_if_valid(grouped_data, output_folder_path, file[:-4], data_points_per_group)

def main():
    # 输入路径、输出路径和每组数据点的数量
    input_dir = r'D:\Project\20240502\降落\out2'
    output_dir = r'D:\Project\20240502\降落\out3'
    data_points_per_group = 15  # 每组数据点的数量
    skip_points = 1  # 采集一组数据点后需要跳过的数据点数量

    # 调用函数处理文件夹
    process_folder(input_dir, output_dir, data_points_per_group, skip_points)

if __name__ == "__main__":
    main()