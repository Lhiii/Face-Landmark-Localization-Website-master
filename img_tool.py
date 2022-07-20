import os
from werkzeug.utils import secure_filename
import random
from datetime import datetime


# 判断文件名是否是我们支持的格式
def allowed_file(filename, config):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config['ALLOWED_EXTENSIONS']


def imgStream(img_local_path):
    """
  工具函数:
  获取本地图片流
  :param img_local_path:文件单张图片的本地绝对路径
  :return: 图片流
  """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode('ascii')
    return img_stream


def saveImg(upload_image, config):
    filename = secure_filename(upload_image.filename)

    random_num = random.randint(0, 100)
    # f.filename.rsplit('.', 1)[1] 获取文件的后缀
    updateName = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(random_num) + "." + filename.rsplit('.', 1)[1]

    Path = os.path.abspath(".") + config['UPLOAD_FOLDER'] + updateName
    upload_image.save(Path)
    return Path, updateName
