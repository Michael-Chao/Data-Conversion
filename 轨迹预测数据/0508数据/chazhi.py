import os
import pandas as pd

input_folder = r'D:\Project\Convert_Dataset\轨迹预测数据\0508数据\2_noParking_0508'
output_folder = r'D:\Project\Convert_Dataset\轨迹预测数据\0508数据\3_chazhi_0508'

# 遍历文件夹中的每个文件
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_folder, file_name)
        print(f"正在处理文件：{file_path}")

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 将-10替换为NaN
        df.replace(-10, float('nan'), inplace=True)

        # 对航向角进行循环插值，这里使用'spline'方法并指定order=3
        if 'TA' in df.columns:
            df['TA'] = df['TA'].interpolate(method='spline', order=3, limit_direction='forward')

            # 处理周期性数据
            df['TA'] = df['TA'].apply(lambda x: (x + 360) % 360 if pd.isna(x) else x)

        # 对地速进行线性插值
        if 'GS' in df.columns:
            df['GS'] = df['GS'].interpolate(method='linear', limit_direction='forward')

        # 保存处理后的数据
        output_file_path = os.path.join(output_folder, file_name)
        df.to_csv(output_file_path, index=False)
