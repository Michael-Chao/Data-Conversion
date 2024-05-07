import json
import os
import matplotlib.pyplot as plt

# 文件路径
file_path = r'D:\Project\Convert_Dataset\fusiondata\filter_ADSB\20220711_1.txt'

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    # 读取整个文件内容
    data_content = file.read()

# 解析JSON数组
data_array = json.loads(data_content)

# 初始化列表来存储经纬度数据
latitudes = []
longitudes = []

# 遍历JSON数组中的每个对象
for data_obj in data_array:
    # 提取经纬度信息
    lat = float(data_obj['LAT'])
    lon = float(data_obj['LON'])
    # 将经纬度添加到列表中
    latitudes.append(lat)
    longitudes.append(lon)
    print(lon, lat)

# 定义保存图像的路径和文件名
save_path = r'D:\Project\Convert_Dataset\interpolated_sampled_ADSB\轨迹图片'
file_name = os.path.basename(file_path).replace('.txt', '') + '.png'
save_file = os.path.join(save_path, file_name)

# 绘制散点图
plt.figure(figsize=(10, 8))
plt.scatter(longitudes[:], latitudes[:], color='blue', marker='o', label='Points')
plt.xlabel('Longitude (LON)')
plt.ylabel('Latitude (LAT)')
plt.title('Scatter Plot of Latitude and Longitude')
plt.legend()
plt.grid(True)

# 设置 y 轴标签格式为固定格式
plt.ticklabel_format(axis='y', style='plain')

# 保存图像
plt.savefig(save_file)

# 显示图像
plt.show()
