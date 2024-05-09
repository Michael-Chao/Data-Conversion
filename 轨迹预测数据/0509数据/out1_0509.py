import os
import pandas as pd
from pathlib import Path


def load_data(file_path):
    """
    Load data from a CSV file and return a DataFrame.

    Args:
        file_path (str): File path.

    Returns:
        pd.DataFrame: DataFrame containing the data.
    """
    df = pd.read_csv(file_path)
    return df


def save_segment(data_segment, output_folder, file_name):
    """
    Save data to a specified file in CSV format.

    Args:
        data_segment (pd.DataFrame): Data segment to be saved.
        output_folder (str): Output folder path.
        file_name (str): Name of the output file.
    """
    folder_path = os.path.join(output_folder, file_name)
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    output_file = os.path.join(folder_path, f"{len(os.listdir(folder_path)) + 1}.csv")
    data_segment.to_csv(output_file, index=False)  # Setting index=False to exclude index column


def clear_existing_files(output_folder, adsb_contents):
    """
    Clear existing files in the specified folder.

    Args:
        output_folder (str): Output folder path.
        adsb_contents (list): List of files to be processed.
    """
    for file_name in adsb_contents:
        folder_path = os.path.join(output_folder, file_name[:-4])
        if os.path.exists(folder_path):
            for existing_file in os.listdir(folder_path):
                existing_file_path = os.path.join(folder_path, existing_file)
                os.remove(existing_file_path)
            print(f"Existing files in {folder_path} have been deleted.")


def process_files(base_path, output_folder, adsb_contents):
    """
    Process files in the given list.

    Args:
        base_path (str): Original folder path.
        output_folder (str): Output folder path.
        adsb_contents (list): List of files to be processed.
    """
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    for file_name in adsb_contents:
        file_path = os.path.join(base_path, file_name)
        data_df = load_data(file_path)

        prev_trp = None
        segment_data = pd.DataFrame()

        for index, row in data_df.iterrows():
            trp = row['TRP']
            lon = row['LON']
            lat = row['LAT']
            gs = row['GS']
            ta = row['TA']

            if prev_trp is not None and abs(trp - prev_trp) > 15:
                save_segment(segment_data, output_folder, file_name[:-4])
                segment_data = pd.DataFrame()

            new_row = pd.DataFrame({'TRP': [trp], 'LON': [lon], 'LAT': [lat], 'GS': [gs], 'TA': [ta]})
            segment_data = pd.concat([segment_data, new_row], ignore_index=True)
            prev_trp = trp

        if not segment_data.empty:
            save_segment(segment_data, output_folder, file_name[:-4])
        print(f"File processed: {file_name}")


def main():
    base_path = r'D:\Project\Convert_Dataset\轨迹预测数据\0509数据\降落\2_deduplication_0508'
    output_folder = r'D:\Project\Convert_Dataset\轨迹预测数据\0509数据\降落\3_out1'

    adsb_contents = ['20220701_1.csv', '20220701_3.csv', '20220703_1.csv', '20220704_1.csv', '20220704_3.csv',
                     '20220706_1.csv', '20220706_3.csv', '20220708_1.csv', '20220710_1.csv']

    # Clear existing files in the output folder
    clear_existing_files(output_folder, adsb_contents)

    # Process files in the original folder and save results to the output folder
    process_files(base_path, output_folder, adsb_contents)


if __name__ == "__main__":
    main()
