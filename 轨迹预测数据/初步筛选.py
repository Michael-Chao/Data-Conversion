import os

input_file_path = r'D:\Project\Convert_Dataset\轨迹预测数据\result_ADSB\20220701.txt'
output_folder_path = r'D:\Project\Convert_Dataset\轨迹预测数据\初步筛选文件夹'
target_addr = "780CE8"

# 确保输出文件夹存在
os.makedirs(output_folder_path, exist_ok=True)

# 打开原始文件，筛选出符合条件的数据并写入新文件
output_file_path = os.path.join(output_folder_path, "20220701.txt")
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    for line in input_file:
        # 将文本按等号分割成键值对
        data = dict(item.split("=") for item in line.strip().split(", "))
        if data.get("ADDR") == target_addr:
            output_file.write(line)

print("筛选完成，文件保存在:", output_file_path)

