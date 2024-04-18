"""
ADSB数据重模块
提供ADSB数据的拟合，并每隔一秒进行重新采样

作者：钞旭
版本：1.0
日期：2024-04-16
"""

import numpy as np
from scipy.interpolate import interp1d
import json
from pathlib import Path
import os
import matplotlib.pyplot as plt


# 绘制原始数据
def plot_original_data(data):
    """
    绘制原始ADS-B数据的经纬度图

    参数:
    data: 包含时间戳、经度和纬度的数据列表
    """
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
    """
    绘制插值后的ADS-B数据的经纬度图

    参数:
    timestamps: 时间戳列表
    sampled_lons: 插值后的经度列表
    sampled_lats: 插值后的纬度列表
    """
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
    """
    绘制原始数据与插值数据的对比图

    参数:
    data: 原始数据列表
    timestamps: 时间戳列表
    sampled_lons: 插值后的经度列表
    sampled_lats: 插值后的纬度列表
    """
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
def load_data(file_path):
    """
    读取ADSB文件并处理数据

    参数:
    file_path: 文件路径

    返回:
    data: 处理后的数据列表，包含时间戳、经度和纬度
    """
    data = []
    with open(file_path, 'r') as file:
        data_list = json.load(file)
        for entry in data_list:
            timestamp = float(entry['TRP'])  # 使用TRP字段作为时间戳
            lon = float(entry['LON'])
            lat = float(entry['LAT'])
            data.append((timestamp, lon, lat))
    return data

# 对数据进行插值拟合
def interpolate_data(data):
    """
    对数据进行插值拟合

    参数:
    data: 数据列表，包含时间戳、经度和纬度

    返回:
    lon_interp: 经度插值函数
    lat_interp: 纬度插值函数
    """
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
    """
    每隔一秒进行采样

    参数:
    lon_interp: 经度插值函数
    lat_interp: 纬度插值函数

    返回:
    timestamps: 采样后的时间戳列表
    sampled_lons: 采样后的经度列表
    sampled_lats: 采样后的纬度列表
    """
    start_time = min(lon_interp.x[0], lat_interp.x[0])
    end_time = max(lon_interp.x[-1], lat_interp.x[-1])
    timestamps = np.arange(start_time, end_time, 1)  # 每隔一秒生成一个时间戳
    sampled_lons = lon_interp(timestamps)
    sampled_lats = lat_interp(timestamps)
    return timestamps, sampled_lons, sampled_lats

def save_sampled_data(timestamps, lons, lats, output_folder):
    """
    保存采样后的数据

    参数:
    timestamps: 时间戳列表
    lons: 经度列表
    lats: 纬度列表
    output_folder: 输出文件夹路径
    """
    if len(timestamps) > 0:
        output_dir = os.path.dirname(output_folder)
        os.makedirs(output_dir, exist_ok=True)  # 创建目录，如果不存在则创建

        # 获取当前文件夹下的文件数
        existing_files = os.listdir(output_folder)
        num_existing_files = len(existing_files)

        # 获取文件名的索引，以便连续命名文件
        output_file_index = num_existing_files + 1

        # 拼接输出文件路径
        output_file_path = os.path.join(output_folder, f"{output_file_index}.txt")

        # 保存数据
        with open(output_file_path, 'w') as file:
            for i in range(len(timestamps)):
                file.write(f"{timestamps[i]}, {lons[i]}, {lats[i]}\n")

        print(f"保存文件 {output_file_path} 成功。")
    else:
        print(f"数据为空，跳过保存。")

def process_files(base_path, output_folder):
    """
    处理所有文件夹

    参数:
    base_path: 输入文件夹路径
    output_folder: 输出文件夹路径
    """
    for subfolder_name in os.listdir(base_path):
        subfolder_path = os.path.join(base_path, subfolder_name)
        if os.path.isdir(subfolder_path):
            process_subfolder(subfolder_path, output_folder)
            print('\n')

def process_subfolder(subfolder_path, output_folder):
    """
    处理单个文件夹

    参数:
    subfolder_path: 子文件夹路径
    output_folder: 输出文件夹路径
    """
    subfolder_name = os.path.basename(subfolder_path)
    folder_path = os.path.join(output_folder, subfolder_name)
    if os.path.exists(folder_path):
        for existing_file in os.listdir(folder_path):
            existing_file_path = os.path.join(folder_path, existing_file)
            os.remove(existing_file_path)
        print(f"已删除 {folder_path} 中的现有文件.")
    print(f"正在处理 {subfolder_name} 文件夹...")
    for filename in os.listdir(subfolder_path):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(subfolder_path, filename)
            process_file(input_file_path, folder_path)

def process_file(input_file_path, output_folder):
    """
    处理单个文件

    参数:
    input_file_path: 输入文件路径
    output_folder: 输出文件夹路径
    """
    # 加载数据
    data = load_data(input_file_path)

    # 对数据进行插值拟合
    lon_interp, lat_interp = interpolate_data(data)

    # 进行采样
    timestamps, sampled_lons, sampled_lats = sample_data(lon_interp, lat_interp)

    # 检查是否数据为空
    if len(timestamps) > 0:
        # 保存采样结果
        save_sampled_data(timestamps, sampled_lons, sampled_lats, output_folder)
    else:
        print(f"文件 {input_file_path} 中的数据为空，跳过保存。")

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
    """
    主函数，负责调度处理过程
    """
    base_path = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\adsb_cut'
    output_folder = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\resampled_ADSBcut'

    # 创建输出文件夹（如果不存在）
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # 处理所有文件
    process_files(base_path, output_folder)


if __name__ == "__main__":
    main()
