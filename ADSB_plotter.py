# import json
# import os
# import matplotlib.pyplot as plt
#
# base_path = r'D:\Project\Convert_Dataset\fusiondata\filter_ADSB'
# adsb_contents = ['20220701_1.txt', '20220701_2.txt', '20220701_3.txt', '20220701_4.txt',
#                  '20220703_1.txt', '20220703_2.txt', '20220703_3.txt', '20220703_4.txt',
#                  '20220704_1.txt', '20220704_2.txt', '20220704_3.txt', '20220704_4.txt',
#                  '20220706_1.txt', '20220706_2.txt', '20220706_3.txt', '20220706_4.txt',
#                  '20220708_1.txt', '20220708_2.txt', '20220708_3.txt', '20220708_4.txt',
#                  '20220710_1.txt', '20220710_2.txt', '20220710_4.txt',
#                  '20220711_1.txt', '20220711_2.txt', '20220711_4.txt',
#                  '20220713_2.txt',
#                  '20220715_1.txt', '20220715_2.txt',
#                  '20220718_4.txt',
#                  '20220719_2.txt',
#                  '20220720_2.txt',
#                  '20220724_4.txt',
#                  '20220729_2.txt']
# adsb_path = os.path.join(base_path, adsb_contents[20])
# with open(adsb_path, 'r', encoding='utf-8') as file:
#     # 读取整个文件内容
#     data_content = file.read()
#
# # 解析JSON数组
# data_array = json.loads(data_content)
#
# # 初始化列表来存储经纬度数据
# latitudes = []
# longitudes = []
#
# # 遍历JSON数组中的每个对象
# for data_obj in data_array:
#     # 提取经纬度信息
#     lat = float(data_obj['LAT'])
#     lon = float(data_obj['LON'])
#     # 将经纬度添加到列表中
#     latitudes.append(lat)
#     longitudes.append(lon)
#
# # 绘制散点图
# plt.figure(figsize=(10, 8))
# plt.scatter(longitudes, latitudes, color='blue', marker='o', label='Points')
# plt.xlabel('Longitude (LON)')
# plt.ylabel('Latitude (LAT)')
# plt.title('Scatter Plot of Latitude and Longitude')
# plt.legend()
# plt.grid(True)
# plt.show()

import json
import os
import matplotlib.pyplot as plt

# 基础路径
base_path = r'D:\Project\Convert_Dataset\fusiondata\filter_ADSB'
# 文件名列表
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
                 '20220724_4.txt',
                 '20220729_2.txt']

# 遍历文件名列表
for file_name in adsb_contents:
    # 构建文件路径
    adsb_path = os.path.join(base_path, file_name)

    # 读取文件内容
    with open(adsb_path, 'r', encoding='utf-8') as file:
        # 读取整个文件内容
        data_content = file.read()

    # 解析JSON数组
    data_array = json.loads(data_content) if data_content else []

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

    # 绘制散点图
    plt.figure(figsize=(10, 8))
    plt.scatter(longitudes, latitudes, color='blue', marker='o', label=file_name)
    plt.xlabel('Longitude (LON)')
    plt.ylabel('Latitude (LAT)')
    plt.title(f'Scatter Plot of Latitude and Longitude for {file_name}')
    plt.legend()
    plt.grid(True)

    # 显示图形
    plt.show()  # 如果你想在一个图形中显示所有点，可以取消这里的注释