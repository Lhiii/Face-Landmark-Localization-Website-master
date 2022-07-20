import base64
import os

import paddlehub as hub
import cv2
from matplotlib import pyplot as plt, image as mpimg


# def cv2_to_base64(image):
#     data = cv2.imencode('.jpg', image)[1]
#     return base64.b64encode(data.tostring()).decode('utf8')

def getFaceLandmarkLocalizationImage(image):
    # img = './face-img/1.jpg'
    src_img = cv2.imread(image)
    face_landmark = hub.Module(name="face_landmark_localization")
    result = face_landmark.keypoint_detection(images=[src_img])

    tmp_img = src_img.copy()
    for i in range(len(result[0]['data'])):
        for index, point in enumerate(result[0]['data'][i]):
            # cv2.putText(img, str(index), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_COMPLEX, 3, (0,0,255), -1)
            cv2.circle(tmp_img, (int(point[0]), int(point[1])), 2, (0, 0, 255), -1)

    return tmp_img
    # res_img_path = os.path.abspath(".") + '/res-img/' + filename
    # cv2.imwrite(res_img_path, tmp_img)

    # img = mpimg.imread(res_img_path)
    # # 展示预测68个关键点结果
    # plt.figure(figsize=(8, 8))
    # plt.imshow(img)
    # plt.axis('off')
    # plt.show()
    # return res_img_path
