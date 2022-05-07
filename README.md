# 这里是ocg-bot使用指南哟~

当前版本尚在初期，功能和使用上尚不完善qwq，请轻点蹂躏~
## 0.文件准备
进入https://github.com/fireinsect/ocg-bot 点上⭐并下载ocg-bot主体

将ygo内pics文件夹拖入ocg-bot/src/static中（配置图片文件）

## 1.安装Python

前往 https://www.python.org/ 下载python，并添加进环境变量
Windows系统下载专供Windows的python，如果的linux系统选择下载Linux用python，并按照Linux的方法配置环境变量。

## 2.运行项目

1. 进入cmd界面或者powershell界面，通过cd进入项目文件夹。

2. 在控制台输入

   ```shell
   python --version
   ```

   确认python是否正确安装

3. 之后在控制台输入

   ```shell
   pip install -r requirements.txt
   ```

   安装依赖，之后可以输入

   ```shell
   python bot.py
   ```

   运行机器人

   如果Linux 需要持续挂起，可以考虑nohup &方法和screen来实现后台挂起

运行成功后，我们需要和CQ-HTTP进行连接

## 3.连接CQ-HTTP

前往 https://github.com/Mrs4s/go-cqhttp > Releases，下载CQ-HTTP的对应操作系统的执行文件。cq在初次运行时会询问代理方式，我们使用反向websocket代理来实现qq机器人。

之后设置自己的qq号与密码来完成cq的部署。

之后我们的bot上会显示连接成功的讯息，这就代表机器人部署成功了



## 4.额外说明

注意的是bot.py和go-cqhttp都需要后台持续挂起才能持续使用机器人，所以我推荐使用云服务器来达成持续使用的效果（需要一定计算机基础）

Windows环境下，go-cqhttp可以通过双击go-cqhttp.bat文件打开。

在Linux环境下，通过控制台输入./go-cqhttp来打开，我推荐使用screen方法来挂起，nohup信息为文件输入，不适合登录。。。





bot随缘更新，有意向的小伙伴可以联系我来一起开发。

bot中使用的卡片查询接口在文件中已经标识，随去随用（不过我的服务器老小水管了，轻点使用谢谢！）

特别感谢：

>萨菲罗斯、红莲魔兽、果冻 
 
提供的支持