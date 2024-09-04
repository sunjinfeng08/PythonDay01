"""
URL configuration for day02 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('dept_list/', views.dept_list),
    path('dept_add/', views.dept_add),
    path('dept_delete/', views.dept_delete),
    path('dept/<int:deptId>/dept_edit/', views.dept_edit),
    path('user_list/', views.user_list),
    path('user_add/',views.user_add),
    path('user/<int:userId>/user_edit/',views.user_edit),
    path('user/<int:userId>/user_delete/',views.user_delete),

    path('test/staticDirector/', views.teststaticDirector),
    path('admin/listadmin/', views.admin_list),
]
