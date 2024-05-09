import os
from pathlib import Path
from scipy.interpolate import interp1d
import numpy as np

class ADSBDataProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def load_data(self, file_path):
        """
        读取ADSB文件并处理数据

        参数:
        file_path: 文件路径

        返回:
        data: 处理后的数据列表，包含时间戳、经度、纬度和状态
        """
        data = []
        with open(file_path, 'r') as file:
            for line in file:
                values = line.strip().split(',')
                timestamp = float(values[0])
                lon = float(values[1])
                lat = float(values[2])
                state = float(values[3])
                data.append([timestamp, lon, lat, state])  # 将每行数据存储为列表

        # 转换为 NumPy 数组
        data = np.array(data)

        return data

    def interpolate_and_resample(self, data):
        """
        对数据进行插值拟合，并每隔一秒进行重新采样

        参数:
        data: 数据列表，包含时间戳、经度、纬度和状态

        返回:
        lon_interp: 经度插值函数
        lat_interp: 纬度插值函数
        """
        timestamps = [entry[0] for entry in data]
        lons = [entry[1] for entry in data]
        lats = [entry[2] for entry in data]
        states = [entry[3] for entry in data]

        # 在这里插入你的插值代码
        # 将插值函数返回给 lon_interp 和 lat_interp
        lon_interp = interp1d(timestamps, lons, kind='linear', fill_value="extrapolate")
        lat_interp = interp1d(timestamps, lats, kind='linear', fill_value="extrapolate")

        return lon_interp, lat_interp

    def process_files(self):
        """
        处理所有文件夹
        """
        for folder_name in os.listdir(self.input_folder):
            folder_path = os.path.join(self.input_folder, folder_name)
            if os.path.isdir(folder_path):
                self.process_folder(folder_path)

    def process_folder(self, folder_path):
        """
        处理单个文件夹

        参数:
        folder_path: 文件夹路径
        """
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                self.process_file(file_path)

    def process_file(self, file_path):
        """
        处理单个文件

        参数:
        file_path: 文件路径
        """
        print(f"处理文件: {file_path}")

        # 加载数据
        data = self.load_data(file_path)

        # 对数据进行插值拟合
        lon_interp, lat_interp = self.interpolate_and_resample(data)

        # 进行重新采样
        start_time = min(data, key=lambda x: x[0])[0]
        end_time = max(data, key=lambda x: x[0])[0]
        resampled_timestamps = list(range(int(start_time), int(end_time) + 1))

        resampled_lons = lon_interp(resampled_timestamps)
        resampled_lats = lat_interp(resampled_timestamps)

        # 保存插值后的数据到输出文件夹
        output_folder = os.path.join(self.output_folder, os.path.basename(os.path.dirname(file_path)))
        Path(output_folder).mkdir(parents=True, exist_ok=True)

        output_file_path = os.path.join(output_folder, os.path.basename(file_path))
        with open(output_file_path, 'w') as f:
            for timestamp, lon, lat, state in zip(resampled_timestamps, resampled_lons, resampled_lats, data[:, 3]):
                f.write(f"{timestamp},{lon},{lat},{state}\n")

        print(f"保存文件: {output_file_path}")


def main():
    input_folder = r'D:\Project\20240502\降落\out1'
    output_folder = r'D:\Project\20240502\降落\out2'

    # 创建数据处理器实例
    processor = ADSBDataProcessor(input_folder, output_folder)

    # 处理所有文件
    processor.process_files()


if __name__ == "__main__":
    main()
