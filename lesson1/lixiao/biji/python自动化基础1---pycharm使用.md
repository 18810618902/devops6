## Python自动化基础

### 第1章 python环境部署

#### 1.1 安装`python`
<pre>
[root@linux-node2 ~]# yum -y install openssl-devel python-devel zlib*
</pre>

#### 1.2 安装`pip`工具,并且让List优雅显示
<pre>
[root@linux-node2 ~]# mkdir /tools
[root@linux-node2 ~]# cd /tools/
[root@linux-node2 tools]# wget https://bootstrap.pypa.io/get-pip.py
[root@linux-node2 tools]# ll
total 1560
-rw-r--r-- 1 root root 1595408 Nov  7  2016 get-pip.py
[root@linux-node2 tools]# python get-pip.py

[root@linux-node2 ~]# mkdir ~/.pip
[root@linux-node2 ~]# cd .pip/
[root@linux-node2 .pip]# vim pip.conf
  [global]
  trusted-host=pypi.douban.com 
  index-url = http://pypi.douban.com/simple 
  [list] #pip list的格式更优雅
  format=columns
</pre>
#### 1.3 配置沙盒环境
<pre>
[root@linux-node2 tools]# pip install virtualenv

[root@linux-node2 tools]# mkdir /data
[root@linux-node2 data]# virtualenv venv
New python executable in /data/venv/bin/python
Installing setuptools, pip, wheel...done.

[root@linux-node2 venv]# source bin/activate
(venv) [root@linux-node2 venv]#
</pre>
#### 1.4 安装`django`
<pre>
(venv) [root@linux-node2 ~]# pip install django==1.11
Collecting django==1.11
  Downloading Django-1.11-py2.py3-none-any.whl (6.9MB)
    100% |████████████████████████████████| 6.9MB 29kB/s 
Collecting pytz (from django==1.11)
  Downloading pytz-2017.3-py2.py3-none-any.whl (511kB)
    100% |████████████████████████████████| 512kB 21kB/s 
Installing collected packages: pytz, django
Successfully installed django-1.11 pytz-2017.3
</pre>
#### 1.5 安装`Pycharm`
> 1.5.1 Windows端安装过程.....略

> 1.5.2 配置`Pycharm`环境

##### 1)创建新项目

![image](https://github.com/cupid-lx/gitdir/blob/master/image/1.png?raw=true)

##### 2)创建一个django项目，选择已有的项目

![image](https://github.com/cupid-lx/gitdir/blob/master/image/2.png?raw=true)

##### 3)添加远程服务器

![image](https://github.com/cupid-lx/gitdir/blob/master/image/3.png?raw=true)

![image](https://github.com/cupid-lx/gitdir/blob/master/image/4.png?raw=true)

##### 4)创建生成

![image](https://github.com/cupid-lx/gitdir/blob/master/image/5.png?raw=true)

##### 5)设置本地目录和远程服务器目录

![image](https://github.com/cupid-lx/gitdir/blob/master/image/6.png?raw=true)

##### 6)创建成功

![image](https://github.com/cupid-lx/gitdir/blob/master/image/7.png?raw=true)

##### 7)设置访问地址

![image](https://github.com/cupid-lx/gitdir/blob/master/image/8.png?raw=true)

![image](https://github.com/cupid-lx/gitdir/blob/master/image/9.png?raw=true)

##### 8)启动连接

![image](https://github.com/cupid-lx/gitdir/blob/master/image/10.png?raw=true)

> 在上图中，红色的警告是提示我们执行'python manage.py migrate'命令，`migrate`是让我们在修改Model后，可以在不影响现有数据的前提下重建表结构。重构之后：

![image](https://github.com/cupid-lx/gitdir/blob/master/image/11.png?raw=true)

#### 1.6 目录说明

> 在上图之中，可以看到myweb项目，里面包含了几个`.py`结尾的文件

<pre>
└── myweb					//项目容器
    ├── manage.py			//命令行工具，让你以各种方式与Django项目进行交互
    ├── myweb
    │   ├── __init__.py		//一个空文件，告诉python项目是一个Python包
    │   ├── settings.py		//Django项目的全局配置文件
    │   ├── urls.py			//Django项目的全局URL声明，request请求会先走这个入口
    │   ├── wsgi.py			//用于你的项目与WSGI兼容的web服务器的入口
    └── templates			//模版文件目录，用来存放html文件
</pre>

### 第2章 环境使用

#### 2.1 创建一个django项目

<pre>
1）使用Pycharm创建
 打开pycharm ---> 选择file ---> New Project,其他设置如1.5

2）使用命令创建：
(venv) [root@linux-node2 reboot6]# ll
total 0
drwxr-xr-x 5 root root 78 Jan  1 06:53 myweb
(venv) [root@linux-node2 reboot6]# django-admin.py startproject myproject
(venv) [root@linux-node2 reboot6]# ll
total 0
drwxr-xr-x 3 root root 38 Jan  1 07:05 myproject
drwxr-xr-x 5 root root 78 Jan  1 06:53 myweb
</pre>

#### 2.2 创建一个app

> 创建一个app，首先要进入项目目录下，然后执行创建命令。一般一个项目有多个app，通用的app也可以在多个项目中使用

<pre>
1) pycharm创建app
打开pycharm ---> 选择Tools ---> 选择Run manage.py Task选项 ---> 在pycharm下方打开的窗口输入 startapp app_name 完成创建

2) 在linux端使用命令创建
(venv) [root@linux-node2 reboot6]# cd myproject/  		//进入项目
(venv) [root@linux-node2 myproject]# ll
total 4
-rwxr-xr-x 1 root root 807 Jan  1 07:05 manage.py
drwxr-xr-x 2 root root  70 Jan  1 07:05 myproject
(venv) [root@linux-node2 myproject]# pwd				//路径展现
/reboot6/myproject
(venv) [root@linux-node2 myproject]# python manage.py startapp app_name //命令创建
(venv) [root@linux-node2 myproject]# ll
total 4
drwxr-xr-x 3 root root 116 Jan  1 07:14 app_name	
-rwxr-xr-x 1 root root 807 Jan  1 07:05 manage.py
drwxr-xr-x 2 root root 108 Jan  1 07:14 myproject
</pre>

<font color='red'>
***项目和app之间的关系：***

***1. myproject是一个项目，myapp是一个应用***

***2. 一个项目下面可以有多个应用（app）***

***3. 在python里，应用相当于一个模块，可以被Include，和import***

***4. 项目跟应用是多对多的关系，也可以是一对一的关系***
</font>

#### 2.3 配置INSTALLED_APPS

每个新创建的app都必须在settings.py配置文件的INSTALLED_APPS里注册，才可以使用

<pre>
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]
</pre>

#### 2.4 url()函数
> Django url() 可以接收四个参数，分别是两个必选参数：regex、view 和两个可选参数：kwargs、name，接下来详细介绍这四个参数。

- regex: 正则表达式，与之匹配的 URL 会执行对应的第二个参数 view。
- view: 用于执行与正则表达式匹配的 URL 请求。
- kwargs: 视图使用的字典类型的参数。
- name: 用来反向获取 URL。

urls.py配置格式
<pre>
urlpatterns = patterns('视图前缀',  
    url(r'^正则表达式1/$', '视图函数1', name="url标识1"),  
    url(r'^正则表达式2/$', '视图函数2', name="url标识2"),  
) 
</pre>

#### 2.3 django的请求过程

> 请求 ---> web服务器(WSGI) ---> django中间件 ---> 路由系统(urls) ---> 视图函数

#### 2.4 访问首页

> 配置好django之后，访问首页，一般会提示一个信息，页面无法访问。先修改项目的`settings.py`配置文件来解决

<pre>
ALLOWED_HOSTS = []，修改为
ALLOWED_HOSTS = ['*']		//允许所有主机访问

<font color='red'>
ALLOWED_HOSTS是为了限定请求中的host值,以防止黑客构造包来发送请求.只有在列表中的host才能访问.强烈建议不要使用*通配符去配置,另外当DEBUG设置为False的时候必须配置这个配置.否则会抛出异常.配置模板如下:

ALLOWED_HOSTS = [
    '.example.com',  # Allow domain and subdomains
    '.example.com.',  # Also allow FQDN and subdomains
]</font>
</pre>
