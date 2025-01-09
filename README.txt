# 本地环境安装
anaconda、pycharm、python、navicat

# 使用方法
1、使用pycharm打开项目文件夹，右下角选择Python解释器
2、安装项目需要的依赖库，在requirements.txt中
3、京东平台如果cookie过期，请将compare/jd.py的cookie更换(需先登录京东平台)
4、在pycharm的teminal下输入命令，启动项目：
python manage.py runserver
5、浏览器登录http://120.0.0.1:8000/
6、进入登录界面，输入账号和密码（账号：admins  密码：admins）
7、进入后台，在浏览器地址后面加/admin，即：
http://127.0.0.1:8000/admin
账号：admins  密码：admins