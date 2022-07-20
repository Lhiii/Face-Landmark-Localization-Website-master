# Face-Landmark-Localization-Website-master

## 一、信息介绍

结合 PaddleDetection blazeface_1000e 人脸检测模型和 PaddleHub face_landmark 模型实现人脸关键点检测。

#### 1. 基于 face_landmark 模型实现的三个功能

* 人脸关键点检测
* 《你的名字》动漫中的图片与目标对象进行换脸
* **AI** 人像美颜

#### 2. 基于 Flask 实现 Web UI 的展示

#### 3. **使用** **TypeScript** **开发**

## 二、环境准备

* conda
* cuda 和 cuDNN
* PaddlePaddle
* PaddleHub
* Typescript

### 安装环境

#### PaddlePaddle 安装

根据具体的Python版本创建Anaconda虚拟环境：

```
conda create -n paddle_env python=3.7
```

进入Anaconda虚拟环境：

```
activate paddle_env
```

在安装 cuda 和 cuDNN 后，根据相应版本安装GPU版的PaddlePaddle：

```
conda install paddlepaddle-gpu==2.3.1 cudatoolkit=10.2 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/
```

验证安装：

```
import paddle
paddle.utils.run_check()
```

如果出现  `PaddlePaddle is installed successfully!`，说明已成功安装。

#### PaddleHub 安装

```
hub install face_landmark_localization
```

#### Typescript 安装

本地环境已经安装了 npm 工具，使用以下命令进行安装。

使用国内镜像：

```
npm config set registry https://registry.npmmirror.com
```

安装 typescript：

```
npm install -g typescript
```

验证安装

```
tsc -v
```

如果出现  `Version 3.2.2`，说明已成功安装。

#### Flask 安装

```
pip install flask
```

使用 **flask** 命令或者 python 的 `-m` 开关来运行 APP.py 应用，最后在浏览器中打开 http://127.0.0.1:5000/ 即可看到运行界面。

## 三、效果展示

* 首页页面

  ![image-20220720120916796](Lhiii/Face-Landmark-Localization-Website-master\sources\image-20220720120916796.png)

* 网页介绍页面

  ![image-20220720121013948](H:\Windows\Desktop\project\sources\image-20220720121013948.png)

* 人脸关键点检测页面

  ![image-20220720121033601](H:\Windows\Desktop\project\sources\image-20220720121033601.png)

* 《你的名字》动漫图换脸页面

  ![image-20220720121113878](H:\Windows\Desktop\project\sources\image-20220720121113878.png)

* **AI** 人像美颜

![image-20220720121139333](H:\Windows\Desktop\project\sources\image-20220720121139333.png)

## 四、版本信息

* 1.0.0

  初始版本
