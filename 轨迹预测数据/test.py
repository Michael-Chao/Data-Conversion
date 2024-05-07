import matplotlib.pyplot as plt

# 定义文件路径
file_path = r'D:\Project\Convert_Dataset\轨迹预测数据\初步筛选文件夹\20220701.txt'

# 初始化用于存储数据的列表
lons = []
lats = []

# 尝试打开并读取文件
try:
    with open(file_path, 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 尝试解析每一行数据
            if line.strip():  # 确保不处理空行
                parts = line.split(', ')  # 假设数据是以逗号和空格分隔的
                record = {}
                for part in parts:
                    if '=' in part:  # 确保每个部分都有键和值
                        key, value = part.split('=')
                        # 根据键名将值转换为适当的类型
                        if key == 'LON':
                            record['LON'] = float(value.strip())
                        elif key == 'LAT':
                            record['LAT'] = float(value.strip())

                # 将经纬度添加到列表中，如果它们都存在的话
                if 'LON' in record and 'LAT' in record:
                    lons.append(record['LON'])
                    lats.append(record['LAT'])

    # 绘制第3353个索引之后的数据点
    index = 3353
    if index < len(lons) and index < len(lats):
        # 绘制散点图
        plt.figure(figsize=(10, 6))
        plt.scatter(lons[index:], lats[index:], color='blue', alpha=0.6, label='Trajectory Points after Index 3353')

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Trajectory Points on Map (Index 3354+)')
        plt.grid(True)
        plt.legend()
        plt.show()
    else:
        print(f"索引 {index} 超出了数据的范围。")

except FileNotFoundError:
    print(f"文件 {file_path} 未找到。")
except Exception as e:
    print(f"读取文件或解析数据时发生错误: {e}")