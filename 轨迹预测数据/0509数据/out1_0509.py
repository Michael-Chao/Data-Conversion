import os
import json
from pathlib import Path
import pandas as pd


def load_data(file_path):
    """
    Load data from an Excel file and return a DataFrame.

    Args:
        file_path (str): File path.

    Returns:
        pd.DataFrame: DataFrame containing the data.
    """
    df = pd.read_excel(file_path)
    return df


def save_segment(data_segment, output_folder, file_name):
    """
    Save data to a specified file without header.

    Args:
        data_segment (pd.DataFrame): Data segment to be saved.
        output_folder (str): Output folder path.
        file_name (str): Name of the output file.
    """
    folder_path = os.path.join(output_folder, file_name)
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    output_file = os.path.join(folder_path, f"{len(os.listdir(folder_path)) + 1}.txt")
    data_segment.to_csv(output_file, index=False, header=False)  # 设置 header=False 不保存标题行


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
            state = row['STATE']

            if prev_trp is not None and abs(trp - prev_trp) > 15:
                save_segment(segment_data, output_folder, file_name[:-4])
                segment_data = pd.DataFrame()

            new_row = pd.DataFrame({'TRP': [trp], 'LON': [lon], 'LAT': [lat], 'STATE': [state]})
            segment_data = pd.concat([segment_data, new_row], ignore_index=True)
            prev_trp = trp

        if not segment_data.empty:
            save_segment(segment_data, output_folder, file_name[:-4])
        print(f"File processed: {file_name}")


def main():
    base_path = r'D:\Project\20240502\降落\改进的01234'
    output_folder = r'D:\Project\20240502\降落\out1'

    adsb_contents = ['20220701_1.xlsx', '20220701_3.xlsx', '20220703_1.xlsx', '20220704_1.xlsx',
                     '20220706_1.xlsx', '20220706_3.xlsx', '20220708_1.xlsx', '20220710_1.xlsx']

    # Clear existing files in the output folder
    clear_existing_files(output_folder, adsb_contents)

    # Process files in the original folder and save results to the output folder
    process_files(base_path, output_folder, adsb_contents)


if __name__ == "__main__":
    main()
