import os
import random
from datetime import datetime

import cv2
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from beautyFace import getBeautyFace
from face_landmark_localization_api import getFaceLandmarkLocalizationImage
from img_tool import saveImg, imgStream, allowed_file
from yourNameFace import getYourNameFace

# app.debug = True
app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = '/face-img/data/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'JPG', 'jpg', 'jpeg', 'gif'}  # 集合类型


@app.route('/detail')
def detail():
    return render_template('detail.html')


@app.route('/faceLocalizationMark')
def faceLocalizationMark():
    image_url_before = imgStream("./sources/1.jpg")
    image_url_after = imgStream("./sources/face_landmark.jpg")
    return render_template('faceLocalizationMark.html', result="人脸关键点的例图�?, image_url_before=image_url_before, image_url_after=image_url_after)


@app.route('/faceLocalizationMark', methods=['POST'])
def getMarkFaceRes():
    upload_image = request.files['file']
    if upload_image and upload_image.filename != '' and allowed_file(upload_image.filename, app.config):
        Path, updateName = saveImg(upload_image, app.config)
        # resImage = getYourNameFace(Path)
        # resPath = os.path.abspath(".") + '/res-img/res_your_name/' + updateName
        resImage = getFaceLandmarkLocalizationImage(Path)
        resPath = os.path.abspath(".") + '/res-img/res_mark_face/' + updateName
        cv2.imwrite(resPath, resImage)

        image_url_before = imgStream(Path)
        image_url_after = imgStream(resPath)
        return render_template('faceLocalizationMark.html', result=upload_image.filename,
                               image_url_before=image_url_before, image_url_after=image_url_after)
    else:
        return render_template('faceLocalizationMark.html', result="invalid image")


@app.route('/yourName')
def yourName():
    image_url_before = imgStream("./sources/single_face3.jpg")
    image_url_after = imgStream("./sources/yourname.jpg")
    return render_template('yourName.html', result="《你的名字》换脸后的例图：", image_url_before=image_url_before, image_url_after=image_url_after)


@app.route('/yourName', methods=['POST'])
def getYourNameFaceRes():
    upload_image = request.files['file']
    if upload_image and upload_image.filename != '' and allowed_file(upload_image.filename, app.config):
        Path, updateName = saveImg(upload_image, app.config)
        resImage = getYourNameFace(Path)
        resPath = os.path.abspath(".") + '/res-img/res_your_name/' + updateName
        cv2.imwrite(resPath, resImage)

        image_url_before = imgStream(Path)
        image_url_after = imgStream(resPath)
        return render_template('faceLocalizationMark.html', result=upload_image.filename,
                               image_url_before=image_url_before, image_url_after=image_url_after)
    else:
        return render_template('yourName.html', result="invalid image")


@app.route('/beautyFace')
def beautyFace():
    image_url_before = imgStream("./sources/4.jpg")
    image_url_after = imgStream("./sources/beautyFace.jpg")
    return render_template('beautyFace.html', result="人像美颜后的例图�?, image_url_before=image_url_before, image_url_after=image_url_after)


@app.route('/beautyFace', methods=['POST'])
def getBeautyFaceRes():
    upload_image = request.files['file']
    if upload_image and upload_image.filename != '' and allowed_file(upload_image.filename, app.config):
        Path, updateName = saveImg(upload_image, app.config)
        resImage = getBeautyFace(Path)
        resPath = os.path.abspath(".") + '/res-img/res_beauty_face/' + updateName
        cv2.imwrite(resPath, resImage)

        image_url_before = imgStream(Path)
        image_url_after = imgStream(resPath)
        return render_template('faceLocalizationMark.html', result=upload_image.filename,
                               image_url_before=image_url_before, image_url_after=image_url_after)
    else:
        return render_template('beautyFace.html', result="invalid image")


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
