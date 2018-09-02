# 微信小游戏《加减大师》辅助
![language-python](https://img.shields.io/badge/language-python-blue.svg)

## 游戏介绍
「加减大师」是腾讯推出的一款微信小游戏，玩家需要在指定时间内判断所给算式的对错，每周比赛排名前500就可以赢得一张大师卡，一定量的大师卡可以兑换物品。

<div align="center">
    <img src="./Images/game1.jpg" height="250">
    <img src="./Images/game2.jpg" height="250">
    <img src="./Images/autoplay.gif" height="250">
    <img src="./Images/succeed.jpg" height="200">
</div>

**WechatGameAutoPlayer** 是用 python 语言实现的一个小脚本，通过 ADB 从手机获得游戏界面截图，然后进行字符识别并判断所给等式的对错，实现自动点击。

## 效果展示
GFM 不支持嵌入网页视频，我在 Zhihu 里发的一篇分享里有发效果录屏。[点击进入](https://zhuanlan.zhihu.com/p/36387916)

## 使用方法
+ 配置 ADB，Windows 系统需另装 ADB 驱动并将可执行文件加入到环境变量 Path 中。这一步是为了后面连接电脑并投屏。

+ 克隆/下载代码到本地
    ```
    $ git clone https://github.com/clouduan/WechatGameAutoPlayer.git --depth=1
    ```

+ 安装所需的包

    首先需要安装 `pyHook` 包，在 [此处](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook) 下载，然后用 `pip` 安装。

    然后执行

    ```
    $ sudo pip3 install -r requirements.txt
    ```
+ ~~将手机调到游戏界面，运行 AutoPlay.py 文件即可~~ ADB 太慢了，直接在手机上操作的话，无法对付最后几题，于是采用投屏方法。

+ 将手机调到第一题界面，用投屏软件将手机画面投到电脑上。这里推荐使用 [Vysor](https://vysor.io/)，目前提供 Windows/MacOSX 客户端和 Chrome 应用，推荐使用 Chrome 应用，好处是跨平台而且方便。

+ 先用相关软件测量包含等式的矩形区域的坐标（左上角的xy值和右下角的xy值），以及 √ 或 × 区域的坐标值，并填入 Config.py 中的相应位置。所用的工具 Windows 上推荐用系统自带画图软件，Linux 可以用 Gimp。矩形区域的选取很重要，可以参考下图标记的区域：

![sample.png](Images/sample.png)

+ 运行 AutoPlayPC.py 即可。

## 实现原理
+ ~~ADB: 获取手机游戏界面截图，并对截图进行灰度化和二值化处理~~
+ 截图：在电脑上对手机等式区域截图，速度很快，极大减小耗时。
+ 字符识别：字符识别没有采用普遍的机器学习方法，而是采用一种叫感知哈希算法（PHA）的相似图片匹配法。在 [CaptchaRecognizer](https://github.com/clouduan/CaptchaRecognizer)中有利用其识别验证码的实现。具体做法简述如下：

    先二值化图像，然后横向分割为两部分，再对每一部分进行纵向分割，得到单个字符（数字和运算符号）。将每个字符图片用一种特定的 hash 函数计算 hash 值，与预先储存的该字符的 hash 值比对（计算汉明距离），汉明距离最小的项所对应的即是该字符的值。
+ 判断：得到所有字符后，将其顺序连接还原为等式，用 `eval()` 函数判断对错。
+ 点击：根据判断结果点击电脑界面的 √ 或 ×，而投屏软件几乎可以和手机实现同步。

