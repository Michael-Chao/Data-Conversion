import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 文件路径
file_path = r'D:\Project\Convert_Dataset\fusiondata\filter_ADSB\20220715_2.txt'

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    # 读取整个文件内容
    data_content = file.read()

# 解析JSON数组
data_array = json.loads(data_content)

# 初始化列表来存储经纬度和高度数据
latitudes = []
longitudes = []
heights = []

# 遍历JSON数组中的每个对象
for data_obj in data_array:
    # 检查'LAT'、'LON'和'GH'字段是否存在
    if 'LAT' in data_obj and 'LON' in data_obj and 'GH' in data_obj:
        # 提取经纬度和高度信息
        lat = float(data_obj.get('LAT', 0))
        lon = float(data_obj.get('LON', 0))
        height = float(data_obj.get('GH', 0))
        # 如果经纬度和高度不为0，则将其添加到列表中
        if lat != 0 and lon != 0 and height != 0:
            latitudes.append(lat)
            longitudes.append(lon)
            heights.append(height)

# 创建三维图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制散点图
ax.scatter(longitudes, latitudes, heights, color='blue', marker='o')

# 设置坐标轴标签
ax.set_xlabel('Longitude (LON)')
ax.set_ylabel('Latitude (LAT)')
ax.set_zlabel('Height (GH)')

# 设置初始视角
ax.view_init(elev=30, azim=45)

# 启用交互式模式
plt.ion()
plt.show()

# 循环等待用户交互
while True:
    # 交互式改变视角
    azim = int(input("Enter azim angle (0-360): "))
    elev = int(input("Enter elev angle (0-180): "))
    ax.view_init(elev=elev, azim=azim)
    plt.draw()
