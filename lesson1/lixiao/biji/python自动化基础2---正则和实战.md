## Python自动化基础

### 3. url获取参数的几种方式

#### 3.1 手动创建访问首页

- 新建views.py视图文件

<pre>
from django.http.response import HttpResponse	//导入函数

def firstpage(request):
    return HttpResponse('hello django')
</pre>

- urls.py函数设置

<pre>
from .views import firstpage		//导入函数

urlpatterns = [
    url(r'^$', firstpage, name='home'),	//设置路由
]

 http://192.168.56.12:9999访问，正确显示hello django
</pre>

#### 3.2 创建app,使用二级域名访问

- 创建myapp

- myapp创建成功，在其目录下创建urls.py配置文件

- 全局myweb/urls.py文件中配置

<pre>
from django.conf.urls import url,include 	//导入include
urlpatterns = [
    url(r'^myapp/', include('myapp.urls')),	//将myapp的urls文件引入
]
</pre>

- myapp/urls.py文件配置

<pre>
from django.conf.urls import url
from .views import hello		//导入视图文件中的hello模块

urlpatterns = [
    url(r'^hello', hello),		//设置路由
]
</pre>

- myapp/views.py文件配置

<pre>
from __future__ import unicode_literals
from django.http.response import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse('hello world')
</pre>

- 访问http://192.168.56.12:9999/myapp/hello

#### 3.3 urls.py正则表达式

![](https://github.com/cupid-lx/gitdir/blob/master/image/20.png?raw=true)

![](https://github.com/cupid-lx/gitdir/blob/master/image/21.png?raw=true)

![](https://github.com/cupid-lx/gitdir/blob/master/image/22.png?raw=true)

![](https://github.com/cupid-lx/gitdir/blob/master/image/23.png?raw=true)


#### 3.4 获取url中的id
- myapp/urls.py配置文件

<pre>
from .views import *
urlpatterns = [
    url(r'^hello', hello),
    <font color='red'>url(r'^user/(\d+)', user),</font>	//匹配任意数字
    <font color='red'>url(r'^user/(\d*)', user),</font>	//匹配0个或多个任意数字
    <font color='red'>url(r'^user/(\w+)', user),</font>	//匹配任意字母和数字
    <font color='red'>url(r'^user/(\d{1,3})', user),</font>	//匹配3位数以内的数字
    <font color='red'>url(r'^user/(\d{3})', user),</font> //只匹配3位数的数字
    ==============隐式位置参数(get方式)=========
]
</pre>

- myapp/views.py配置文件

<pre>
def user(request,pk):		//pk主键
    print pk
    return HttpResponse(pk)
</pre>

- 访问http://192.168.56.12:9999/myapp/user/234,正确返回234

#### 3.5 让url后面的两个数字参数相加并正常显示

- views.py配置

<pre>
def add(request, n1,n2):
    return HttpResponse(int(n1)+int(n2))
</pre>

- urls.py配置

<pre>
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^add/(\d{1,2})/(\d{1,2})$',add),
]
</pre>

- 访问http://192.168.56.12/myapp/add/2/3,正确显示5

#### 3.6 进阶

- urls.py配置

<pre>
from .views import *
urlpatterns = [
    <font color='red'>url(r'users/(?P《res》d+)', users),</font>
    url(r'^users/(?P《res》\d+)/(?P《ok》\d+)',users),
	//?P是固定的的参数
	//res是在views视图函数里的一个字典的key，以字典的形式获取
]
</pre>

- views.py配置

<pre>
def users(request, **kwargs):
    result = kwargs.get('res')
    return HttpResponse(result)

def users(request, **test):
    result = test.get('res')
    comm = test.get('ok')
    return HttpResponse("res is %s,comm is %s" %(result,comm))
</pre>

#### 3.7 获取url中的值

- urls.py配置

<pre>
urlpatterns = [
    url(r'^hello', hello),
    url(r'^user/(\d+)',user),
    url(r'^add/(\d{1,2})/(\d{1,2})$',add),
    url(r'^users/(?P<res>\d+)/(?P<ok>\d+)',users),
    url(r'^artest', artest),
]
</pre>

- views.py配置

<pre>
from django.http.response import JsonResponse

def artest(request):
    name = request.GET.get('name')
    uid = request.GET.get('id')
    result = {'username':name,'id':uid}
    return JsonResponse(result)
</pre>

- 访问http://192.168.56.12:9999/myapp/artest/?name=reboot&id=12，返回json串


- random.randint(1,99) ------> 获取随机数