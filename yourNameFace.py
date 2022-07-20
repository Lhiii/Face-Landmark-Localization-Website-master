import os
import zipfile
import cv2
import paddlehub as hub
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math


def getYourNameFace(image):
    src_img = cv2.imread(image)

    module = hub.Module(name="face_landmark_localization")
    detection_result = module.keypoint_detection(images=[src_img])

    # 解压图片数据
    # path_zip = "./face-img/your_name.zip"  # 所需图片的存放路径
    # z = zipfile.ZipFile(path_zip, "r")  # 读取zip文件
    # num_Image = len(z.namelist()) - 1  # 总的图片数量
    #
    # # 数据解压 注：每次重启环境运行，都需要重新解压
    # path_Image = './face-img/'
    # with zipfile.ZipFile(path_zip, 'r') as zin:
    #     zin.extractall(path_Image)

    path_Images = './face-img/your_name/out'
    # 参数定义每张图片最后最短边所占的像素长度
    single_image_len = 10
    num_Image = 638

    # 压缩图像至固定大小
    def pic_compression(src_pic):
        target_high = src_pic.shape[0]
        target_weight = src_pic.shape[1]
        if target_high < target_weight:
            target_weight = np.ceil(target_weight / (target_high / single_image_len))
            target_high = single_image_len
        else:
            target_high = np.ceil(target_high / (target_weight / single_image_len))
            target_weight = single_image_len

        return cv2.resize(src_pic, (int(target_weight), int(target_high))), target_high, target_weight

    # 计算图像的RGB特征
    feature_dim = 3  # 特征维度 R、G、B 共三维
    pic_feature = np.zeros([num_Image, feature_dim])  # 特征向量
    for indexImg in range(3, num_Image + 3 - 1):  # 图片索引由3开始
        path_pic = path_Images + str(indexImg) + '.png'  # 获取每张图片的地址
        pic = cv2.imread(path_pic)
        pic_comed, th, tw = pic_compression(pic.copy())  # 计算得到压缩图像
        # 在此尝试只计算单通道的特征
        # for idx in range(0,feature_dim):
        for idx in range(0, 1):
            pic_feature[indexImg - 3, idx] = np.average(pic_comed[:-1, :-1, idx])

    print(th, tw)

    num_face = len(detection_result[0]['data'])
    left_p = [None for _ in range(num_face)]
    right_p = [None for _ in range(num_face)]
    top_p = [None for _ in range(num_face)]
    bottom_p = [None for _ in range(num_face)]
    ROI_Image = [None for _ in range(num_face)]
    for i in range(len(detection_result[0]['data'])):
        points = np.mat(detection_result[0]['data'][i])
        # 获取待重组的矩形局域的两个坐标值
        point_a = np.floor(np.amin(points, axis=0))
        point_d = np.ceil(np.amax(points, axis=0))

        # 抠出待组合区域图像
        left_p[i] = int(point_a[0, 0])
        right_p[i] = int(point_d[0, 0])
        top_p[i] = int(point_a[0, 1])
        bottom_p[i] = int(point_d[0, 1])
        # 得到目标图像
        temp_Image = src_img.copy()
        ROI_Image[i] = temp_Image[top_p[i]:bottom_p[i], left_p[i]:right_p[i]]

        block_feature = np.zeros(feature_dim)  # 每一图块的特征
        blo_fea_buff = np.zeros(num_Image)  # 缓存每一图块特征到所有图片特征的欧式距离值
        for idx_i in range(0, len(ROI_Image[i]) - int(th), int(th)):
            for idx_j in range(0, len(ROI_Image[i][1]) - int(tw), int(tw)):
                # 计算当前图块的颜色特征
                # 在此尝试只计算单通道的特征
                # for idx in range(0,feature_dim):
                for idx in range(0, 1):
                    block_feature[idx] = np.average(ROI_Image[i][idx_i:idx_i + int(th), idx_j:idx_j + int(tw), idx])
                # 计算当前图块到所有图片集图片在颜色空间的欧式距离
                for img_idx in range(0, num_Image):
                    blo_fea_buff[img_idx] = np.linalg.norm(block_feature - pic_feature[img_idx])

                pic_idx = np.argmin(blo_fea_buff) + 3  # 获取到最小欧式距离的图片索引

                path_pic = path_Images + str(int(pic_idx)) + '.png'
                pic = cv2.imread(path_pic)
                pic_comed, _, _ = pic_compression(pic.copy())  # 计算得到压缩图像
                ROI_Image[i][idx_i:idx_i + int(th), idx_j:idx_j + int(tw)] = pic_comed  # 将压缩过后的图像贴到待组合的区域图上

    def mask(image, face_landmark, i):
        """
        image： 人像图片
        face_landmark: 人脸关键点
        """
        # image_cp = image.copy()
        hull = cv2.convexHull(face_landmark)

        cv2.fillPoly(image, [hull], (0, 0, 0))
        for idx_i in range(top_p[i], bottom_p[i]):
            for idx_j in range(left_p[i], right_p[i]):
                if (image[idx_i, idx_j] == [0, 0, 0]).all():
                    image[idx_i, idx_j] = ROI_Image[i][idx_i - top_p[i], idx_j - left_p[i]]

        return image

    # 获取人脸关键点数据，和原始图像
    result_image = src_img.copy()
    for i in range(num_face):
        face_landmark = np.array(detection_result[0]['data'][i], dtype='int')
        result_image = mask(result_image, face_landmark, i)

    return result_image
