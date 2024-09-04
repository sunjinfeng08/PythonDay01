from lib2to3.fixes.fix_input import context

from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from django.template.defaultfilters import title

from app01 import models
from app01.models import UserInfo
from django.utils.safestring import mark_safe
from app01.utils.pageination import Pageination
# Create your views here.
def dept_list(request):
    # 获取部门表所有信息
    queryDeptSet = models.Department.objects.all()
    for dept in queryDeptSet:
     deptname = dept.title
    # print(deptname)
    return render(request,'dept_list.html',{'queryDeptSet':queryDeptSet})
def dept_add(request):
    if request.method =="GET":
        return render(request,'dept_add.html')
# 获取前端界面传过来的数据
    title = request.POST.get('title')
    models.Department.objects.create(title=title)
    return redirect("/dept_list/")
def dept_delete(request):
    dept_id = request.GET.get('dept_id')
    models.Department.objects.filter(id=dept_id).delete()
    return redirect("/dept_list/")
def dept_edit(request,deptId):
    if request.method =="GET":
        print(deptId)
        dept_edit_row = models.Department.objects.filter(id=deptId).first()
        title = dept_edit_row.title
        return render(request,'dept_edit.html',{'dept_edit_row':dept_edit_row})
    title2 = request.POST.get('title')
    models.Department.objects.filter(id=deptId).update(title=title2)
    return redirect("/dept_list/")
def user_list_pageDone(request):
    data_dict = {}
    searchValue = request.GET.get('userSerach')
    if searchValue is  None:
        searchValue = ""
    if searchValue:
        data_dict["name__contains"] = searchValue
    # queryUserList = models.UserInfo.objects.all()
    page = int(request.GET.get('page', '1'))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size
    queryUserList = models.UserInfo.objects.filter(**data_dict).order_by('id')[start:end]
    totalPageSize =models.UserInfo.objects.filter(**data_dict).order_by('id').count()
    totalPageCount,div = divmod(totalPageSize,page_size)
    if div > 0 :
        totalPageCount = totalPageCount +1
    plus = 5
    if totalPageSize <= 2 * plus + 1:
        start_page = 1
        end_page = totalPageCount
    else:
        if page <= plus:
           start_page = 1
           end_page = 2 * plus + 1
        else:
            if (page + plus) > totalPageCount:
                start_page = totalPageCount - 2*plus
                end_page = totalPageCount
            else:
                start_page = page - plus
                end_page = page + plus + 1
    # <li><a href="#">1</a></li>
    page_str_list=[]
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    if page > 1:
        prev ='<li><a href="?page={}">上一页</a></li>'.format(page -1)
    else:
        prev=''
    page_str_list.append(prev)
    for i in range(start_page,end_page + 1):
        if i == page:
            ele ='<li class="active"><a href="?page={}">{}</a></li>'.format(i,i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele )
    if page < totalPageCount:
        nextpage ='<li><a href="?page={}">下一页</a></li>'.format(page +1)
    else:
        nextpage=''
    page_str_list.append(nextpage)
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(totalPageCount))
    page_string = mark_safe(" ".join(page_str_list))

    return render(request,'user_list.html',{'queryUserList':queryUserList,"searchValue":searchValue,"page_string":page_string})
def user_list(request):
    data_dict = {}
    searchValue = request.GET.get('userSerach')
    if searchValue is None:
        searchValue = ""
    if searchValue:
        data_dict["name__contains"] = searchValue
    queryset = models.UserInfo.objects.filter(**data_dict).order_by('id')
    page_object = Pageination(request,queryset)
    page_queryset = page_object.querypageset
    page_string = page_object.html()
    context={
        "searchValue": searchValue,
        'queryUserList': page_queryset,
        "page_string": page_string
    }
    return render(request,'user_list.html',context)
'''
最原始的编写方法
def user_add(request):
    if request.method =="GET":
        contextParameter = {
             'genderchoose' : models.UserInfo.gender_choices,
             'deptList' : models.Department.objects.all()
        }
        return render(request,'user_add.html',contextParameter)
    return  redirect("/user_list/")
'''
from django import  forms
class UserModelForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields=["name","password","age","account","create_time","depart_id","gender"]
        '''
        三种用法
        fields ="__all__" 展示所有字段
        exclude = ['password'] 排除某个或多个字段
        '''
        # widgets = {
        #     'name': forms.TextInput(attrs={'class':'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class':'form-control'}),
        #     'age': forms.TextInput(attrs={'class':'form-control'}),
        #     'account': forms.TextInput(attrs={'class':'form-control'}),
        #     'create_time': forms.TextInput(attrs={'class':'form-control'}),
        #     'depart_id': forms.Select(attrs={'class':'form-control'}),
        #     'gender': forms.Select(attrs={'class':'form-control'}),
        # }

    #把bootstrap的样式添加到前端页面
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            # if name =="password":
            #     continue
            field.widget.attrs = {'class':'form-control',"placeholder":field.label}
#     验证字段格式方式二
    def clean_age(self):
        txt_age = self.cleaned_data['age']
        if int(txt_age) < 18:
            raise ValidationError("年龄必须大于18")
        return txt_age
    def clean_name(self):
        # 检验输入的数据是否在数据库表中已存在
        txt_name = self.cleaned_data['name']
        exists =models.UserInfo.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()
        if exists:
            raise ValidationError("用户名已被占用")
        return txt_name
def user_add(request):
    if request.method =="GET":
        form = UserModelForm()
        return render(request,'user_add.html', {"form":form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user_list/")
    else:
        print(form.errors)
    return render(request, 'user_add.html', {"form": form})
def user_edit(request,userId):
    if request.method == "GET":
        currentRowValue = models.UserInfo.objects.filter(id=userId).first()
        form = UserModelForm(instance=currentRowValue)
        return render(request,'user_edit.html',{"form": form})
    updateRowValue = models.UserInfo.objects.filter(id=userId).first()
    form = UserModelForm(data=request.POST,instance=updateRowValue)
    if form.is_valid():
        form.save()
        return redirect("/user_list/")
    else:
        print(form.errors)
    return render(request,'user_edit.html',{"form":form})
def user_delete(request,userId):
    models.UserInfo.objects.filter(id=userId).delete()
    return redirect("/user_list/")

def teststaticDirector(request ):
    return render(request,'testStatic.html')
def admin_list(request):
    queryAdminSet = models.Admin.objects.all()
    return render(request,'adminlist.html',{'queryAdminSet':queryAdminSet})