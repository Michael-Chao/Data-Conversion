import cv2
import matplotlib.pyplot as plt
import os


video_dir = r'E:\experiment\fusion\data_process\selected_video\202207'
video_dir_img = r'G:\selected_imgs'
if not os.path.exists(video_dir):
    os.makedirs(video_dir)

for video_name_dir in sorted(os.listdir(video_dir)):
    video_name_path = os.path.join(video_dir_img, video_name_dir)
    # if not os.path.exists(video_name_path):
    #     os.makedirs(video_name_path)
    for video_name in sorted(os.listdir(os.path.join(video_dir, video_name_dir))):
        v = os.path.join(video_dir,video_name_dir,video_name)

        # 读取mp4, 抽帧保存
        cap = cv2.VideoCapture()
        cap.open(v)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(fps, width, height)
        suc = cap.isOpened()
        print(suc)

        img_dir_name = video_name[12:-4]
        img_dir = os.path.join(video_dir_img,img_dir_name)
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        img_path = os.path.join(img_dir,'saved_')
        frame_count = 0
        rate = 25  # 每20帧保存一下
        while suc:
            frame_count += 1
            suc, frame = cap.read()
            if frame_count % rate == 0:
                file_name = '{}{:0>5d}.jpg'.format(img_path, frame_count // rate)
                if suc == True:
                    cv2.imwrite(file_name, frame)
                    cv2.waitKey(1)
        cap.release()
        print(video_name + 'Finished!')