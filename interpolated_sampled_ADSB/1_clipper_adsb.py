import os
import json
from pathlib import Path


def load_data(file_path):
    """
    从文件中加载数据并返回JSON对象列表。

    Args:
        file_path (str): 文件路径。

    Returns:
        list: 包含JSON对象的列表。
    """
    with open(file_path, 'r') as file:
        data_list = json.load(file)
    return data_list


def save_segment(data_segment, output_folder, file_name):
    """
    将数据保存到指定的文件中。

    Args:
        data_segment (list): 要保存的数据段列表。
        output_folder (str): 输出文件夹路径。
        file_name (str): 输出文件的名称。
    """
    folder_path = os.path.join(output_folder, file_name)
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    output_file = os.path.join(folder_path, f"{len(os.listdir(folder_path)) + 1}.txt")
    with open(output_file, 'w') as file:
        json.dump(data_segment, file, indent=4)


def clear_existing_files(output_folder, adsb_contents):
    """
    清除指定文件夹中已存在的文件。

    Args:
        output_folder (str): 输出文件夹路径。
        adsb_contents (list): 待处理的文件列表。
    """
    for file_name in adsb_contents:
        folder_path = os.path.join(output_folder, file_name[:-4])
        if os.path.exists(folder_path):
            for existing_file in os.listdir(folder_path):
                existing_file_path = os.path.join(folder_path, existing_file)
                os.remove(existing_file_path)
            print(f"已删除 {folder_path} 中的现有文件.")


def process_files(base_path, output_folder, adsb_contents):
    """
    处理给定文件列表中的文件。

    Args:
        base_path (str): 原始文件夹路径。
        output_folder (str): 输出文件夹路径。
        adsb_contents (list): 待处理的文件列表。
    """
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    for file_name in adsb_contents:
        file_path = os.path.join(base_path, file_name)
        data_list = load_data(file_path)

        prev_trp = None
        segment_data = []

        for entry in data_list:
            trp = entry['TRP']
            lon = entry['LON']
            lat = entry['LAT']

            if prev_trp is not None and abs(trp - prev_trp) > 15:
                save_segment(segment_data, output_folder, file_name[:-4])
                segment_data = []

            segment_data.append({'TRP': trp, 'LON': lon, 'LAT': lat})
            prev_trp = trp

        if segment_data:
            save_segment(segment_data, output_folder, file_name[:-4])
        print(f"已处理文件: {file_name}")


def main():
    base_path = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\filter_ADSB'
    output_folder = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\adsb_cut'

    adsb_contents = ['20220701_1.txt', '20220701_2.txt', '20220701_3.txt', '20220701_4.txt',
                     '20220703_1.txt', '20220703_2.txt', '20220703_4.txt',
                     '20220704_1.txt', '20220704_2.txt', '20220704_3.txt', '20220704_4.txt',
                     '20220706_1.txt', '20220706_2.txt', '20220706_3.txt', '20220706_4.txt',
                     '20220708_1.txt', '20220708_2.txt', '20220708_4.txt',
                     '20220710_1.txt', '20220710_2.txt', '20220710_4.txt',
                     '20220711_2.txt', '20220711_4.txt',
                     '20220713_2.txt',
                     '20220715_2.txt',
                     '20220718_4.txt',
                     '20220719_2.txt',
                     '20220720_2.txt',
                     '20220724_4.txt']

    # takeoff = [0, 2, 4, 10, 12, 14, 16, 20, 23]
    #
    # Landing = [1, 3, 5, 6, 7, 8, 9, 11, 13, 15, 17, 18, 19, 21, 22, 24, 25, 26, 27, 28, 29]

    # 清除输出文件夹中已存在的文件
    clear_existing_files(output_folder, adsb_contents)

    # 处理原始文件夹中的文件，并将处理结果保存到输出文件夹中
    process_files(base_path, output_folder, adsb_contents)


if __name__ == "__main__":
    main()
