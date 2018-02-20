# coding=utf-8
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


class JuncheePaginator(Paginator): #__init__()函数不用说了吧，就是重载了一下，添加了一个range_num参数，代表在可能的情况下，当前页左右各显示多少个页标签，默认值为4。
    def __init__(self, object_list, per_page=10, range_num=4, orphans=0, allow_empty_first_page=True):
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        self.range_num = range_num

    def page(self, number):   #page()函数是对父类Paginator的page()函数的重写，主要是为了记录当前页。
        #self.page_num =int(number)# 获取前端number对应的值
        return super(JuncheePaginator, self).page(number)

    def _page_range_ext(self):
        num_count = 2 * self.range_num + 1  # 底部显示的页码数
        if self.num_pages <= num_count:  #p.num_pages为总页码，如果总页码小于等于底部显示页码，返回range(1,num_page+1)
            return range(1, self.num_pages + 1)
        num_list = []
        num_list.append(self.page_num)
        for i in range(1, self.range_num + 1):
            if self.page_num - i <= 0:
                num_list.append(num_count + self.page_num - i)
            else:
                num_list.append(self.page_num - i)
            if self.page_num + i <= self.num_pages:
                num_list.append(self.page_num + i)
            else:
                num_list.append(self.page_num + i - num_count)
            num_list.sort()
            return num_list

    page_range_ext = property(_page_range_ext)

    def pagecomputer(self, page_num):
        try:
            pagedata = self.page(page_num)
        except PageNotAnInteger:
            pagedata = self.page(1)
        except EmptyPage:
            pagedata = self.page(self.num_pages)
        return pagedata, self.num_pages
