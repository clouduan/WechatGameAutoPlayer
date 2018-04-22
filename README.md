# 微信小游戏《加减大师》辅助
![language-python](https://img.shields.io/badge/language-python-blue.svg)
[![license](https://img.shields.io/github/license/clouduan/WechatGameAutoPlayer.svg)](https://github.com/clouduan/WechatGameAutoPlayer/blob/master/LICENSE)

## 游戏说明
「加减大师」是腾讯推出的一款微信小游戏，玩法极其简单，它给出一个等式，要玩家在指定时间内判断等式的对错，答对40个就算挑战成功，可以赢取娃娃。
游戏界面截图及辅助运行动图如下

<div align="center">
  <img src="./Images/PlusSubstractMaster1.jpg" height="150">
  <img src="./Images/PlusSubstractMaster2.jpg" height="150">
  <img src="./Images/PlusSubstractMaster3.png" height="150"> 
  <img src="./Images/PlusSubstractMaster4.gif" height="150">
</div>

**WechatGameAutoPlayer** 是用 python 语言实现的一个脚本，可通过 ADB 从手机获得游戏界面截图，然后进行字符识别并判断所给等式的对错，实现自动点击。本脚本系一时娱乐之作，开心就好~~~
## 使用方法
+ 配置 ADB，Windows 系统需另装 ADB 驱动并将可执行文件加入到环境变量 Path 中

+ 克隆代码到本地
```
$ git clone https://github.com/clouduan/WechatGameAutoPlayer.git
```

+ 安装所需的包
```
$ sudo pip3 install -r requirements.txt
```

+ 将手机调到游戏界面，运行 AutoPlay.py 文件即可

## 实现原理
+ ADB: 获取手机游戏界面截图，并对截图进行灰度化和二值化处理
+ PIL.Image: 截取等式出现的区域，先横向分割为两部分，再对每一部分进行纵向分割，得到单个字符（数字和运算符号）
+ Numpy.array: 将每个字符图片用一种特定的方法计算 hash 值，与预先处理并储存的字符 hash 值比对（计算汉明距离），汉明距离最小的项所对应的即是该字符的值。得到所有字符后，将其顺序连接还原为等式，用 `eval()` 函数判断对错
+ ADB: 根据判断结果点击手机界面的 √ 或 ×

## Todo
- [ ] 速度问题，这是个亟待解决的问题。详情参见[Issue-2](https://github.com/clouduan/WechatGameAutoPlayer/issues/2)
- [ ] 适配 IOS 系统
- [ ] 适配不同屏幕尺寸的手机
