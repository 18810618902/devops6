# 作业：完成用户登录，和退出界面，用户登录认证


## 目录结构
<pre>
├── accounts          # 用户
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py        # 用户url配置
│   ├── views.py        # 用户视图
├── app1
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py        
│   ├── views.py
├── dashboard           # dashboard项目
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py          # dashboard的url配置
│   ├── views.py          # dashboard视图
├── manage.py
├── myweb1                # 主项目
│   ├── __init__.py
│   ├── settings.py       # 全局配置文件
│   ├── urls.py           # 全局url配件
│   ├── wsgi.py
├── static               # 静态文件
└── templates            # html文件
    ├── index2.html
    ├── index.html
    ├── pages
    │   ├── examples
    │   │   ├── 404.html
    │   │   ├── 500.html
    │   │   ├── blank.html
    │   │   ├── invoice.html
    │   │   ├── invoice-print.html
    │   │   ├── lockscreen.html
    │   │   ├── login.html
    │   │   ├── pace.html
    │   │   ├── profile.html
    │   │   └── register.html
    
  </pre>
  
  
  ### 项目分析
  
  用户登录：
         前端 ：表单ajax psot提交，用户名，密码
         后端： 接收用户名，密码，然后鉴权，
               用户名密码正确： 返回状态码0，跳转dashboard主页。
               错误：返回状态码1，留在登录界面
  
  用户登出：
         前端 ：<a>标签发送一个get请求给后端
         后端： 执行logout方法，并跳转到login界面
 
 dashboard主页：
           访问根页面，直接跳转到dashboard主页
           用户登录验证：
                   通过 ： 访问dashboard主页
                   不通过：跳转到login界面
 
