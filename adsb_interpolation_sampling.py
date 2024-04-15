import numpy as np
from scipy.interpolate import interp1d
import json
from pathlib import Path
import os


# 读取ADSB文件并处理数据
def load_data(file_path):
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
def save_sampled_data(timestamps, lons, lats, output_file):
    with open(output_file, 'w') as file:
        for i in range(len(timestamps)):
            file.write(f"{timestamps[i]}, {lons[i]}, {lats[i]}\n")


def process_files(base_path, adsb_contents, output_folder):
    for file_name in adsb_contents:
        input_file_path = os.path.join(base_path, file_name)
        output_file_path = os.path.join(output_folder, file_name)
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


# 主函数
def main():
    # file_path = r'D:\Project\Convert_Dataset\fusiondata\filter_ADSB\20220701_1.txt'  # 替换为你的ADSB文件路径
    # output_file = r'D:\Project\Convert_Dataset\fusiondata\test_adsb.txt'  # 保存采样结果的文件路径

    base_path = r'D:\Project\Convert_Dataset\fusiondata\filter_ADSB'
    output_folder = r'D:\Project\Convert_Dataset\resampled_ADSB'

    # 创建输出文件夹（如果不存在）
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    adsb_contents = ['20220701_1.txt', '20220701_2.txt', '20220701_3.txt', '20220701_4.txt',
                     '20220703_1.txt', '20220703_2.txt', '20220703_4.txt',
                     '20220704_1.txt', '20220704_2.txt', '20220704_3.txt', '20220704_4.txt',
                     '20220706_1.txt', '20220706_2.txt', '20220706_3.txt', '20220706_4.txt',
                     '20220708_1.txt', '20220708_2.txt', '20220708_4.txt',
                     '20220710_1.txt', '20220710_2.txt', '20220710_4.txt',
                     '20220711_1.txt', '20220711_2.txt', '20220711_4.txt',
                     '20220713_2.txt',
                     '20220715_2.txt',
                     '20220718_4.txt',
                     '20220719_2.txt',
                     '20220720_2.txt',
                     '20220724_4.txt']

    # 处理所有文件
    process_files(base_path, adsb_contents, output_folder)


if __name__ == "__main__":
    main()
