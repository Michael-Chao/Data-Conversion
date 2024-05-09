import os
from pathlib import Path
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd


class ADSBDataProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def load_data(self, file_path):
        """
        读取CSV文件并处理数据
        """
        # 使用pandas读取CSV文件
        df = pd.read_csv(file_path, index_col=0)

        # 返回DataFrame
        return df

    def interpolate_and_resample(self, data):
        """
        对数据进行插值拟合，并每隔一秒进行重新采样
        """
        # 获取时间戳
        timestamps = data.index.values

        # 对每个需要的列进行插值
        columns_to_interpolate = ['LON', 'LAT', 'GS', 'TA']
        interpolated_funcs = {col: interp1d(timestamps, data[col], kind='linear', fill_value="extrapolate") for col in
                              columns_to_interpolate}

        # 进行重新采样
        start_time = timestamps.min()
        end_time = timestamps.max()
        resampled_timestamps = np.arange(start_time, end_time + 1, 1)

        # 使用插值函数进行插值
        resampled_data = {col: interpolated_funcs[col](resampled_timestamps) for col in columns_to_interpolate}

        # 将插值后的数据转换为DataFrame
        resampled_df = pd.DataFrame(resampled_data, index=resampled_timestamps)

        return resampled_df

    def process_files(self):
        """
        处理所有文件夹中的CSV文件
        """
        for folder_path in os.listdir(self.input_folder):
            folder_path_full = os.path.join(self.input_folder, folder_path)
            if os.path.isdir(folder_path_full):
                self.process_folder(folder_path_full)

    def process_folder(self, folder_path):
        """
        处理单个文件夹中的CSV文件
        """
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder_path, file_name)
                self.process_file(file_path)

    def process_file(self, file_path):
        """
        处理单个CSV文件
        """
        print(f"处理文件: {file_path}")

        # 加载数据
        data = self.load_data(file_path)

        # 对数据进行插值拟合
        resampled_df = self.interpolate_and_resample(data)

        # 保存插值后的数据到输出文件夹
        output_folder = os.path.join(self.output_folder, os.path.basename(os.path.dirname(file_path)))
        Path(output_folder).mkdir(parents=True, exist_ok=True)

        output_file_path = os.path.join(output_folder, os.path.basename(file_path))
        resampled_df.to_csv(output_file_path)

        print(f"保存文件: {output_file_path}")


def main():
    input_folder = r'D:\Project\Convert_Dataset\轨迹预测数据\0509数据\降落\3_out1'
    output_folder = r'D:\Project\Convert_Dataset\轨迹预测数据\0509数据\降落\4_out2'

    # 创建数据处理器实例
    processor = ADSBDataProcessor(input_folder, output_folder)

    # 处理所有文件
    processor.process_files()


if __name__ == "__main__":
    main()