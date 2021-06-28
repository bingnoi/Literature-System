"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.conf.urls import url
from . import search #导入search.py
from login.views import index,login,register,info,infochange,redict
from review.views import submit
from history.views import recommend,detail,dfind,find,testfind
urlpatterns = [

    #进入系统首页
    url(r'^$', index),

    #登录
    url(r'^login/$',login),

    #注册
    url(r'^register/$',register),

    #搜索
    url(r'^search$', search.search),

    #论文数量排名
    # 直方图统计
    url(r'^echarts.html$', search.Echarts),
    # 地图热图统计
    url(r'^chinamap.html$',search.Chinamap),

    #首页功能(获取session用户名)
    url(r'^searchfirst$', search.search_form),

    #翻页
    url(r'^page$', search.Page),

    #右侧扇形图
    url(r'^echarts-cirle.html$', search.Echscirle),

    #评论入口
    url(r'^insert$', search.insert),

    #提交评论
    url(r'^submit$',submit),

    #推荐论文入口
    url(r'^recommend/$',recommend),

    #知识图谱
    url(r'^graphnpm$', search.Graph),

    #个人信息入口
    url(r'^info/$',info),

    #修改个人信息
    url(r'^infochange$',infochange),

    #修改信息后重定向到首页
    url(r'^redict$',redict),

    #查看详情论文
    url(r'^detail$',detail),

    #论文查找入口
    url(r'^dfind$',dfind),
    #点击查看论文功能
    url(r'^find$',find),
    url(r'^testfind$',testfind),
]
#静态文件处理1.4版本需要
urlpatterns += staticfiles_urlpatterns()
