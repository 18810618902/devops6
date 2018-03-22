# 作业 

## 要求:

- 出版社，作者，书籍功能完善展示
- creatview写一个例子（选做）,把书，出版社，作者的添加操作用createview也实现一次。



1.项目分析：


       1).用户管理
	   
	   	         *.用户登录
				 
	   	         *.用户退出
				 
       2).仪表盘	
	   
       3).图书管理系统   
	   
	   	         *.图书管理
				 
	   	         *.作者管理
				 
	   	         *.出版商管理
				 
2.项目功能分析:

       1).仪表盘
	       
		   apps: dashboard
	           
						类：   LoginView          #用户登录
						 
						类：   LogoutView         #用户退出
						 
						类:    IndexView          #dashboard首页

       2).图书管理系统
	   
		   apps: books
		   
		       包:  book    
					  
					    类:    BookListView       #图书列表,和图书增加功能
					    
					    类:    BookDetailView     #图书,更新,删除功能
						
		       包:  book2

					    类:    BookAddView        #图书添加功能
						  
		       包:  author

					    类:    AuthorListView     #作者列表,和作者添加
					    
					    类:    BookDetailView     #作者,更新,删除功能
				
		       包:  publish
				   
					    类:    PublishListView    #出版商列表,和出版商添加
					    
					    类:    BookDetailView     #出版商,更新,删除功能

							  

3.流程图

![image](https://github.com/1032231418/python/blob/master/lesson10/naotu.png)	   
		   
4.演示

![image](https://github.com/1032231418/python/blob/master/lesson10/yanshi.gif)	   
