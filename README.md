# WechatGameAutoPlayer
微信小游戏《加减大师》助手
## 游戏说明
「加减大师」是腾讯推出的一款微信小游戏，玩法极其简单，它给出一个等式，要玩家在指定时间内判断等式的对错，每答对40个就可以获得娃娃成就。
游戏界面截图如下
<div align="center">
  <img src="./Images/PlusSubstractMaster1.jpg" height="150">
  <img src="./Images/PlusSubstractMaster2.jpg"height="150">
  <img src="./Images/PlusSubstractMaster3.png"height="150"> 
</div>

## 使用方法
+ 克隆代码到本地
```
git clone https://github.com/clouduan/WechatGameAutoPlayer.git
```
+ 安装所需的包
```
sudo pip3 install -r requirements.txt
```
+ 调到游戏界面，运行 AutoPlay.py 文件即可
+ ![玩法动态截图](./Images/PlusSubstractMaster4.gif）

## 实现原理
+ adb 获取手机界面截图
+ 截取等式区域，先横向分割为两部分，再对每一部分进行纵向分割，得到单个字符（数字和运算符号）
+ 将每个字符图片用一种特定的方法计算 hash 值，与预先处理并储存的字符 hash 值比对（计算汉明距离），汉明距离最小的项所对应的即是该字符的值
+ 将每个字符顺序连接成为表达式，用 `eval` 函数判断对错
+ 根据判断结果点击界面对应位置

## Todo
- [ ] 鲁棒性up
