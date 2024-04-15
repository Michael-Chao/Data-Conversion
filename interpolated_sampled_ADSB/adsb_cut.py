import os
import json
from pathlib import Path


def load_data(file_path):
    with open(file_path, 'r') as file:
        data_list = json.load(file)
    return data_list


def save_segment(data_segment, output_folder, file_name):
    folder_path = os.path.join(output_folder, file_name)
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    output_file = os.path.join(folder_path, f"{len(os.listdir(folder_path)) + 1}.txt")
    with open(output_file, 'w') as file:
        for entry in data_segment:
            file.write(json.dumps(entry) + '\n')


def main():
    base_path = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\filter_ADSB'
    output_folder = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\adsb_cut'

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


if __name__ == "__main__":
    main()
