import numpy as np
from scipy.interpolate import interp1d
import json
from pathlib import Path
import os
import matplotlib.pyplot as plt


# 绘制原始数据
def plot_original_data(data):
    timestamps = [entry[0] for entry in data]
    lons = [entry[1] for entry in data]
    lats = [entry[2] for entry in data]

    plt.figure(figsize=(10, 6))
    plt.plot(lons, lats, marker='o', linestyle='', color='b', label='Original Data')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Original ADSB Data')
    plt.legend()
    plt.grid(True)
    plt.show()


# 绘制插值后的数据
def plot_interpolated_data(timestamps, sampled_lons, sampled_lats):
    plt.figure(figsize=(10, 6))
    plt.plot(sampled_lons, sampled_lats, marker='o', linestyle='', color='r', label='Interpolated Data')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Interpolated ADSB Data')
    plt.legend()
    plt.grid(True)
    plt.show()


# 绘制对比图
def plot_comparison(data, timestamps, sampled_lons, sampled_lats):
    timestamps_orig = [entry[0] for entry in data]
    lons_orig = [entry[1] for entry in data]
    lats_orig = [entry[2] for entry in data]

    plt.figure(figsize=(10, 6))
    plt.plot(lons_orig, lats_orig, marker='o', linestyle='', color='b', label='Original Data')
    plt.plot(sampled_lons, sampled_lats, marker='o', linestyle='', color='r', label='Interpolated Data')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Comparison of Original and Interpolated ADSB Data')
    plt.legend()
    plt.grid(True)
    plt.show()


# 读取ADSB文件并处理数据
# def load_data(file_path):
#     data = []
#     with open(file_path, 'r') as file:
#         data_list = json.load(file)
#         for entry in data_list:
#             timestamp = float(entry['TRP'])  # 使用TRP字段作为时间戳
#             lon = float(entry['LON'])
#             lat = float(entry['LAT'])
#             data.append((timestamp, lon, lat))
#     return data

def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            entry = json.loads(line.strip())
            timestamp = float(entry['TRP'])  # 使用TRP字段作为时间戳
            lon = float(entry['LON'])
            lat = float(entry['LAT'])
            data.append((timestamp, lon, lat))
    return data

# 对数据进行插值拟合
def interpolate_data(data):
    timestamps = np.array([entry[0] for entry in data])
    lons = np.array([entry[1] for entry in data])
    lats = np.array([entry[2] for entry in data])

    # 使用线性插值拟合经纬度数据
    lon_interp = interp1d(timestamps, lons, kind='linear')
    lat_interp = interp1d(timestamps, lats, kind='linear')

    # 返回插值函数
    return lon_interp, lat_interp


# 每隔一秒进行采样
def sample_data(lon_interp, lat_interp):
    start_time = min(lon_interp.x[0], lat_interp.x[0])
    end_time = max(lon_interp.x[-1], lat_interp.x[-1])
    timestamps = np.arange(start_time, end_time, 1)  # 每隔一秒生成一个时间戳
    sampled_lons = lon_interp(timestamps)
    sampled_lats = lat_interp(timestamps)
    return timestamps, sampled_lons, sampled_lats


# 保存采样结果
# def save_sampled_data(timestamps, lons, lats, output_file):
#     with open(output_file, 'w') as file:
#         for i in range(len(timestamps)):
#             file.write(f"{timestamps[i]}, {lons[i]}, {lats[i]}\n")
def save_sampled_data(timestamps, lons, lats, output_file):
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)  # 创建目录，如果不存在则创建
    with open(output_file, 'w') as file:
        for i in range(len(timestamps)):
            file.write(f"{timestamps[i]}, {lons[i]}, {lats[i]}\n")


# def process_files(base_path, adsb_contents, output_folder):
#     for file_name in adsb_contents:
#         input_file_path = os.path.join(base_path, file_name)
#         output_file_path = os.path.join(output_folder, file_name)
#         process_file(input_file_path, output_file_path)

def process_files(base_path, output_folder):
    for subfolder_name in os.listdir(base_path):
        subfolder_path = os.path.join(base_path, subfolder_name)
        if os.path.isdir(subfolder_path):
            process_subfolder(subfolder_path, output_folder)

def process_subfolder(subfolder_path, output_folder):
    subfolder_name = os.path.basename(subfolder_path)
    print(f"正在处理 {subfolder_name} 文件夹...")
    for filename in os.listdir(subfolder_path):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(subfolder_path, filename)
            output_file_path = os.path.join(output_folder, os.path.basename(subfolder_path), filename)
            process_file(input_file_path, output_file_path)

def process_file(input_file_path, output_file_path):
    # 加载数据
    data = load_data(input_file_path)

    # 对数据进行插值拟合
    lon_interp, lat_interp = interpolate_data(data)

    # 进行采样
    timestamps, sampled_lons, sampled_lats = sample_data(lon_interp, lat_interp)

    # 保存采样结果
    save_sampled_data(timestamps, sampled_lons, sampled_lats, output_file_path)

    # 绘制原始数据
    # plot_original_data(data)
    #
    # # 绘制插值后的数据
    # plot_interpolated_data(timestamps, sampled_lons, sampled_lats)
    #
    # # 绘制对比图
    # plot_comparison(data, timestamps, sampled_lons, sampled_lats)


# 主函数
def main():
    base_path = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\adsb_cut'
    output_folder = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\resampled_ADSBcut'

    # 创建输出文件夹（如果不存在）
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # 处理所有文件
    process_files(base_path, output_folder)


if __name__ == "__main__":
    main()
