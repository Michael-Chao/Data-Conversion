'''
将数据集转换为 COCO 格式
数据集包括预训练和正常模式的数据集
'''
import os
import json
import cv2
import re
import math

import datetime

DATA_PATH = os.path.abspath('fusiondata')
# print(DATA_PATH)
OUT_PATH = os.path.join(DATA_PATH, 'annotations')

SPLITS = {'mini_train': [3],
          'mini_valuation': [19],
          'train': [1, 2, 6, 7, 9, 10, 12, 15, 16, 19, 20, 21, 22, 23, 24],
          'valuation': [0, 3, 4, 5, 8],
          'test': [11, 13, 14, 17, 18],
          'mini_pretrain': [7, 11, 20],
          'mini_preval': [1, 9, 14],
          'pretrain': [0, 2, 4, 5, 6, 7, 8, 10, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23, 24],
          'preval': [1, 3, 11, 18]
          }

# 是否处于调试模式
DEBUG = False

# 图片和labels的子目录
image_contents = ['2022-07-01-14-31-27_2022-07-01-15-01-30_00.07.25.025-00.12.41.854', '2022-07-01-15-31-33_2022-07-01-16-01-36_00.05.59.014-00.14.35.556',
            '2022-07-01-19-01-54_2022-07-01-19-31-57_00.06.04.364-00.10.37.179', '2022-07-01-19-31-57_2022-07-01-20-02-00_00.13.00.307-00.17.33.231',
            '2022-07-03-13-36-09_2022-07-03-14-06-12_00.00.10.988-00.05.13.173', '2022-07-03-14-06-12_2022-07-03-14-36-15_00.16.27.290-00.21.36.848',
            '2022-07-03-19-36-45_2022-07-03-20-06-48_00.17.22.241-00.23.08.434', '2022-07-04-13-08-28_2022-07-04-13-38-31_00.02.00.857-00.04.47.495',
            '2022-07-04-14-08-34_2022-07-04-14-38-37_00.12.34.663-00.16.52.934', '2022-07-04-18-08-58_2022-07-04-18-39-01_00.26.09.773-00.30.02.400',
            '2022-07-04-19-39-07_2022-07-04-20-09-10_00.03.37.973-00.09.31.492', '2022-07-06-17-43-43_2022-07-06-18-13-46_00.03.26.982-00.08.12.729',
            '2022-07-06-18-13-46_2022-07-06-18-43-49_00.21.58.565-00.29.47.389', '2022-07-06-19-43-55_2022-07-06-20-13-58_00.01.00.446-00.07.01.292',
            '2022-07-08-12-48-01_2022-07-08-13-18-04_00.13.40.495-00.19.08.327', '2022-07-08-13-48-07_2022-07-08-14-18-10_00.19.10.261-00.24.41.785',
            '2022-07-08-18-18-34_2022-07-08-18-48-37_00.20.40.065-00.25.45.960', '2022-07-08-19-48-43_2022-07-08-20-18-46_00.02.13.714-00.10.00.799',
            '2022-07-10-15-23-04_2022-07-10-15-53-07_00.10.50.025-00.15.41.163', '2022-07-10-15-53-07_2022-07-10-16-23-10_00.26.40.912-00.30.02.400',
            '2022-07-10-19-23-28_2022-07-10-19-53-31_00.22.00.660-00.28.27.151', '2022-07-11-12-55-13_2022-07-11-13-25-16_00.01.33.381-00.06.11.696',
            '2022-07-11-13-55-19_2022-07-11-14-25-22_00.16.37.726-00.21.50.774', '2022-07-11-19-25-52_2022-07-11-19-55-55_00.20.29.907-00.26.30.753',
            '2022-07-13-20-00-43_2022-07-13-20-30-46_00.06.03.341-00.13.42.604']

label_contents = ['2022-07-01-14-31-27_2022-07-01-15-01-30-00.07.25.025-00.12.41.854', '2022-07-01-15-31-33_2022-07-01-16-01-36-00.05.59.014-00.14.35.556',
                  '2022-07-01-19-01-54_2022-07-01-19-31-57-00.06.04.364-00.10.37.179', '2022-07-01-19-31-57_2022-07-01-20-02-00-00.13.00.307-00.17.33.231',
                  '2022-07-03-13-36-09_2022-07-03-14-06-12-00.00.10.988-00.05.13.173', '2022-07-03-14-06-12_2022-07-03-14-36-15-00.16.27.290-00.21.36.848',
                  '2022-07-03-19-36-45_2022-07-03-20-06-48-00.17.22.241-00.23.08.434', '2022-07-04-13-08-28_2022-07-04-13-38-31-00.02.00.857-00.04.47.495',
                  '2022-07-04-14-08-34_2022-07-04-14-38-37-00.12.34.663-00.16.52.934', '2022-07-04-18-08-58_2022-07-04-18-39-01-00.26.09.773-00.30.02.400',
                  '2022-07-04-19-39-07_2022-07-04-20-09-10-00.03.37.973-00.09.31.492', '2022-07-06-17-43-43_2022-07-06-18-13-46-00.03.26.982-00.08.12.729',
                  '2022-07-06-18-13-46_2022-07-06-18-43-49-00.21.58.565-00.29.47.389', '2022-07-06-19-43-55_2022-07-06-20-13-58-00.01.00.446-00.07.01.292',
                  '2022-07-08-12-48-01_2022-07-08-13-18-04-00.13.40.495-00.19.08.327', '2022-07-08-13-48-07_2022-07-08-14-18-10-00.19.10.261-00.24.41.785',
                  '2022-07-08-18-18-34_2022-07-08-18-48-37-00.20.40.065-00.25.45.960', '2022-07-08-19-48-43_2022-07-08-20-18-46-00.02.13.714-00.10.00.799',
                  '2022-07-10-15-23-04_2022-07-10-15-53-07-00.10.50.025-00.15.41.163', '2022-07-10-15-53-07_2022-07-10-16-23-10-00.26.40.912-00.30.02.400',
                  '2022-07-10-19-23-28_2022-07-10-19-53-31-00.22.00.660-00.28.27.151', '2022-07-11-12-55-13_2022-07-11-13-25-16-00.01.33.381-00.06.11.696',
                  '2022-07-11-13-55-19_2022-07-11-14-25-22-00.16.37.726-00.21.50.774', '2022-07-11-19-25-52_2022-07-11-19-55-55-00.20.29.907-00.26.30.753',
                  '2022-07-13-20-00-43_2022-07-13-20-30-46-00.06.03.341-00.13.42.604']

adsb_contents = ['20220701_1.txt', '20220701_2.txt', '20220701_3.txt', '20220701_4.txt',
                 '20220703_1.txt', '20220703_2.txt', '20220703_3.txt', '20220703_4.txt',
                 '20220704_1.txt', '20220704_2.txt', '20220704_3.txt', '20220704_4.txt',
                 '20220706_1.txt', '20220706_2.txt', '20220706_3.txt', '20220706_4.txt',
                 '20220708_1.txt', '20220708_2.txt', '20220708_3.txt', '20220708_4.txt',
                 '20220710_1.txt', '20220710_2.txt', '20220710_4.txt', '20220711_1.txt',
                 '20220711_2.txt', '20220711_4.txt', '20220713_2.txt', '20220715_1.txt',
                 '20220715_2.txt', '20220718_4.txt', '20220719_2.txt', '20220720_2.txt',
                 '20220724_4.txt', '20220729_2.txt']

folder_time = ['14:38:52.025000', '15:37:32.014000', '19:07:58.364000', '19:44:57.307000', '13:36:19.988000', '14:22:39.290000', '19:54:07.241000',
               '13:10:28.857000', '14:21:08.663000', '18:35:07.773000', '19:42:44.973000', '17:47:09.982000', '18:35:44.565000', '19:44:55.446000',
               '13:01:41.495000', '14:07:17.261000', '18:39:14.065000', '19:50:56.714000', '15:33:54.025000', '16:19:47.912000', '19:45:28.660000',
               '12:56:46.381000', '14:11:56.726000', '19:46:21.907000', '20:06:46.341000']

# 个人数据集中所有的类别，一共是两种
CATS = ['airliner', 'propelled aircraft']

# 每种类别对应的ID
CAT_IDS = {v: i + 1 for i, v in enumerate(CATS)}

# 数据集的基本信息
DATA_INFO = {
            "year": "2022",
            "version": "1.0",
            "description": "2022年7月的富蕴机场的监控图片及其对应的ADS-B数据",
            "date_created": "2023-12-22",
            "total_images": 8201,
            "total_labels": 8201,
            "total_boxes": 9112}

def _bbox_inside(box1, box2):
    return box1[0] > box2[0] and box1[0] + box1[2] < box2[0] + box2[2] and \
        box1[1] > box2[1] and box1[1] + box1[3] < box2[1] + box2[3]

def read_label_txt(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    lines = content.strip().split('\n')
    label_values = [[float(value) for value in line.split(',')] for line in lines]
    return label_values

def calculate_bbox(x, y, w, h):
    x_min = x
    y_min = y
    x_max = x + w
    y_max = y + h
    return [x_min, y_min, x_max, y_max]

# 计算TRP时间
def calculate_trp_time(file_time):
    file_time_datetime = datetime.datetime.strptime(file_time, "%H:%M:%S.%f")
    adjusted_time = file_time_datetime - datetime.timedelta(hours=8)
    trp_adjusted_time = (adjusted_time - datetime.datetime.combine(adjusted_time.date(), datetime.time.min)).total_seconds()
    return trp_adjusted_time

# 图片文件夹和adsb文件的对应关系
def map_img_to_adsb(image_contents, adsb_contents):
    date_file_mapping = {}

    for date in image_contents:
        date_key = date[:10].replace('-', '')  # Extract the date part and remove hyphens
        matching_files = [file for file in adsb_contents if date_key in file]
        date_file_mapping[date] = matching_files

    return date_file_mapping

# 打印对应关系
def print_date_file_mapping(result):
    num = 0
    for key, value in result.items():
        num += 1
        print(key, ": ",  value)
    print(num)

# 获取对应的经纬度
def get_adsb_data(adsb_txt, adsb_dataset_path, img_TRP_time):
    lon_lat_array = []
    min_diff = math.inf
    min_entry = None
    for file in adsb_txt:
        adsb_path = os.path.join(adsb_dataset_path, file)
        with open(adsb_path, 'r') as f:
            adsb_data = json.load(f)
            found_entry = False
            for entry in adsb_data:
                diff = abs(entry['TRP'] - img_TRP_time)
                if diff < 1 and diff < min_diff:
                    min_diff = diff
                    min_entry = entry
                    found_entry = True
                else:
                    pass
            if found_entry:
                break
    if min_entry is not None:
        lon = min_entry['LON']
        lat = min_entry['LAT']
        adsb_time = min_entry['TRP']
        lon_lat_array = [min_diff, adsb_time, lon, lat]
    return lon_lat_array

def visualize_annotations(img_path, anns):
    img = cv2.imread(img_path)

    for ann in anns:
        bbox = ann['bbox']
        cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2] + bbox[0]), int(bbox[3] + bbox[1])), (0, 0, 255), 3, lineType=cv2.LINE_AA)

    cv2.namedWindow('Image with Label', cv2.WINDOW_NORMAL)
    cv2.imshow('Image with Label', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    if not os.path.exists(OUT_PATH):  # 用于判断某个路径是否存在，如果不存在则创建这个路径
        os.mkdir(OUT_PATH)

    # 建立图片文件夹和ADSB的txt文件之间的映射关系
    date_file_map = map_img_to_adsb(image_contents, adsb_contents)
    # print_date_file_mapping(date_file_map)
    det_list = ['mini_train', 'mini_valuation', 'train', 'valuation', 'test']

    for split, list in SPLITS.items():
        print("正在生成数据集：", split)
        # print(list)
        data_path = DATA_PATH
        out_path = os.path.join(OUT_PATH, '{}.json'.format(split))
        adsb_dataset_path = os.path.join(DATA_PATH, 'filter_ADSB')
        # print(out_path)
        categories_info = [{'name': CATS[i], 'id': i + 1} for i in range(len(CATS))]

        DATA_INFO['version'] = split

        ret = {'info': DATA_INFO, 'images': [], 'annotations': [], 'categories': categories_info}
        '''
        创建coco格式数据，从这里可以看出 coco 格式如下：
        {
          "info": []
          "images": [],
          "annotations": [],
          "categories": [categories_info],		#记录所有目标物体的类别
        }
        '''

        num_images = 0
        num_anns = 0
        '''
        第一个：所有相机拍摄的全部图片数量计数
        第二个：一张图片中有效的 box 个数
        第三个：当前 box 所属的图片 id
        '''

        for i in list:
            img_folder_name = image_contents[i]
            print("正在处理图片文件夹：", img_folder_name)
            img_folder_path = os.path.join(DATA_PATH, 'selected_imgs', img_folder_name)
            # print(img_folder_path)
            label_folder_name = label_contents[i]
            label_folder_path = os.path.join(DATA_PATH, 'labels', label_folder_name)
            # print(label_folder_path)

            # 换算成TRP时间
            file_time = folder_time[i]
            trp_time = calculate_trp_time(file_time)
            # print(trp_time)

            adsb_txt = date_file_map[img_folder_name]
            # print("图片对应的ADS-B文件为：", adsb_txt)

            adsb_data = None
            for img_name in sorted(os.listdir(img_folder_path)):
                if img_name.endswith('.jpg') or img_name.endswith('.png'):
                    image_path = os.path.join('selected_imgs', img_folder_name, img_name)
                    # 图像ID
                    num_images += 1

                    # 图像帧数
                    frame_number = re.search(r'(\d+)', img_name).group(1)
                    # print("正在处理该图片：", image_path)

                    # 图片的TRP时间戳
                    frame_seconds = int(frame_number)
                    img_TRP_time = trp_time + frame_seconds
                    # print(img_time)

                    # 获取该张图片对应的ADS-B数据
                    lon_lat_array = get_adsb_data(adsb_txt, adsb_dataset_path, img_TRP_time)

                    # 一张图像在COCO格式下的所有信息
                    image_info = {'id': num_images,
                                  'file_name': image_path,
                                  'video_name': img_folder_name,
                                  'frame_id': frame_number,
                                  'width': 1280,
                                  'height': 6016,
                                  'img_time': img_TRP_time
                                  }
                    '''
                    创建 COCO 格式的 image_info 的字段，将上面所产生的结果储存在了image_info 字段中，下面解释下每个属性的意义：
                    'id'：图片的id（基于全部的相机图片），唯一标识符
                    'file_name'：图片的文件名
                    'video_name'：属于哪一段视频
                    'frame_id'：图像在视频中的帧数
                    'width'：图片的宽度
                    'height'：图片的高度
                    'img_time': 图像对应的TRP时间
                    '''
                    if split in det_list:
                        # 添加'images'信息
                        ret['images'].append(image_info)

                        # 标签信息
                        anns = []
                        label_name = img_name.replace('.jpg', '.txt')
                        label_path = os.path.join(label_folder_path, label_name)
                        # print(label_path)

                        # 读取标签信息
                        label_data = read_label_txt(label_path)

                        for box in label_data:
                            # 有效box的ID
                            num_anns += 1

                            # box 所属类别的 id
                            track_id = int(box[1])
                            if track_id not in [4, 19]:
                                category_id = 1 # 目标飞机
                            else:
                                category_id = 2 # 螺旋桨飞机

                            # 中心点坐标
                            center_x = box[2] + box[4] / 2
                            center_y = box[3] + box[5] / 2
                            amodel_center = [center_x, center_y]

                            ann = {
                                'id': num_anns,
                                'image_id': num_images,
                                'category_id': category_id,
                                'dim': [box[4], box[5]],
                                'track_id': track_id,
                                'amodel_center': amodel_center,
                                'iscrowd': 0,
                                'bbox': [box[2], box[3], box[4], box[5]],
                                'area': box[4] * box[5],
                                'ann_time': img_TRP_time
                            }
                            '''
                            coco 格式的 ann 字段，一张图片中一个 box 对应一个 ann 字段，属性含义如下：
                            'id': 有效 box 的 id
                            'image_id': 当前 box 所属的图片 id
                            'category_id': box 所属类别的 id
                            'dim': box 的长宽
                            'track_id': 被检测目标物体 box 的 id
                            'amodel_center': 被检测目标的中心点坐标
                            'iscrowd': 是否遮挡
                            'bbox': box的左上角坐标和宽度、高度(x_min, y_min, width, height)
                            'area': bbox的面积
                            'ann_time': 标签时间
                            '''

                            # 添加对应的经纬度
                            if category_id == 1:
                                if lon_lat_array != []:
                                    ann.update({'lon_lat': lon_lat_array})
                                else:
                                    ann.update({'lon_lat': [-1, -1, -1, -1]})
                            elif category_id == 2:
                                ann.update({'lon_lat': [-2, -2, -2, -2]})

                            # 添加每张图片对应的标签
                            anns.append(ann)

                        # 添加标注信息ret['annotations']
                        for ann_info in anns:
                            ret['annotations'].append(ann_info)

                        if DEBUG:
                            img_path = os.path.join(data_path, image_info['file_name'])
                            visualize_annotations(img_path, anns)

                    else:
                        if lon_lat_array != []:
                            # 添加'images'信息
                            image_info['lon_lat'] = lon_lat_array
                            ret['images'].append(image_info)

                            # 标签信息
                            anns = []
                            label_name = img_name.replace('.jpg', '.txt')
                            label_path = os.path.join(label_folder_path, label_name)
                            # print(label_path)

                            # 读取标签信息
                            label_data = read_label_txt(label_path)

                            for box in label_data:
                                # 有效box的ID
                                num_anns += 1

                                # box 所属类别的 id
                                track_id = int(box[1])
                                if track_id not in [4, 19]:
                                    category_id = 1  # 目标飞机
                                else:
                                    category_id = 2  # 螺旋桨飞机

                                # 中心点坐标
                                center_x = box[2] + box[4] / 2
                                center_y = box[3] + box[5] / 2
                                amodel_center = [center_x, center_y]

                                ann = {
                                    'id': num_anns,
                                    'image_id': num_images,
                                    'category_id': category_id,
                                    'dim': [box[4], box[5]],
                                    'track_id': track_id,
                                    'amodel_center': amodel_center,
                                    'iscrowd': 0,
                                    'bbox': [box[2], box[3], box[4], box[5]],
                                    'area': box[4] * box[5],
                                    'ann_time': img_TRP_time
                                }
                                '''
                                coco 格式的 ann 字段，一张图片中一个 box 对应一个 ann 字段，属性含义如下：
                                'id': 有效 box 的 id
                                'image_id': 当前 box 所属的图片 id
                                'category_id': box 所属类别的 id
                                'dim': box 的长宽
                                'track_id': 被检测目标物体 box 的 id
                                'amodel_center': 被检测目标的中心点坐标
                                'iscrowd': 是否遮挡
                                'bbox': box的左上角坐标和宽度、高度(x_min, y_min, width, height)
                                'area': bbox的面积
                                'ann_time': 标签时间
                                '''

                                # 添加对应的经纬度
                                if category_id == 1:
                                    ann.update({'lon_lat': lon_lat_array})

                                # 添加每张图片对应的标签
                                anns.append(ann)

                            # 添加标注信息ret['annotations']
                            for ann_info in anns:
                                ret['annotations'].append(ann_info)

                            if DEBUG:
                                img_path = os.path.join(data_path, image_info['file_name'])
                                visualize_annotations(img_path, anns)

        print('重新排序图像')
        print('{}: {} 张images {} 个boxes'.format(
            split, len(ret['images']), len(ret['annotations'])))
        print('out_path', out_path, '\n')
        print('\n')
        json.dump(ret, open(out_path, 'w'))

if __name__ == '__main__':
    main()
