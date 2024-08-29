from django.utils.safestring import mark_safe
import copy
class Pageination(object):
    def __init__(self,request,queryset,page_size=10,page_param="page",plus =5):
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict=query_dict

        page = request.GET.get(page_param,"1")
        self.page_param=page_param
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.querypageset = queryset[self.start:self.end]
        totalPageSize = queryset.count()
        total_page_count,div =divmod(totalPageSize,page_size)
        if div:
            total_page_count +=1
        self.total_page_count = total_page_count
        self.plus = plus
        self.totalPageSize = totalPageSize
    def html(self):
        if self.totalPageSize <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus + 1
        # <li><a href="#">1</a></li>
        page_str_list = []
        self.query_dict.setlist(self.page_param, [11])
        page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
        if self.page > 1:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(self.page - 1)
        else:
            prev = ''
        page_str_list.append(prev)
        for i in range(start_page, end_page + 1):
            if i == self.page:
                ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)
        if self.page <  self.total_page_count:
            nextpage = '<li><a href="?page={}">下一页</a></li>'.format( self.page + 1)
        else:
            nextpage = ''
        page_str_list.append(nextpage)
        page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(self.total_page_count))
        page_string = mark_safe(" ".join(page_str_list))
        return page_string