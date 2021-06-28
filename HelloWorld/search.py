#返回前端内容的方法
from django.http import HttpResponse
#数据渲染
from django.shortcuts import render_to_response
from django.shortcuts import render
#导入获取新浪新闻、百度介绍函数
from . import News,getbdinfo
import json
#翻页模块
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
#导入数据库对象
from HelloWorld.models import *
#导入存储浏览记录模块
from history.models import user

#导入处理数据并构造图谱的函数
#生成作者-单位处理数据
from other.author_school_possess import getAuthor_School
#处理作者函数
from other.author import getAuthor
#处理作者单位函数
from other.team import getTeam
#构建合作关系函数
from other.cooperation import getCooperation
#构建图谱数据函数
from other.tp_data_pro import getTpData
#统计频次函数
from collections import Counter

#全局变量 不用设置session
val=""#存储搜索主题

#城市信息
global city
city = ['北京', '天津', '上海', '重庆', '河北', '河南', '云南', '辽宁', '黑龙江', '湖南', '安徽', '山东', '新疆', '江苏', '浙江', '江西', '湖北', '广西',
        '甘肃', '山西', '内蒙古', '陕西', '吉林', '福建', '贵州', '广东', '青海', '西藏', '四川', '宁夏', '海南', '台湾', '香港', '澳门']


# 系统首页
def search_form(request):
    #获取session内容并显示
    username = request.session.get('username')
    return render(request,'search.html',{'username':username})

# 接收请求数据
#存储用户浏览记录
def search(request):
    request.encoding='utf-8'
    #global全局变量
    global val
    val = request.GET['q']
    print(val)
    request.session['val'] = val
    username = request.session.get('username')
    if request.GET['q']=='':
        #搜索关键词为空，则返回搜索页面
        return render(request,'search.html',{'username':username})
        #return redirect('/search')
    if len(request.GET['q'])!=0:
        #百度百科对于关键字的介绍
        text = getbdinfo.getBaiDuInfo(val)
        print('baidu text')
        #新浪新闻爬虫展示
        '''
        新浪cookie过期比较快，若页面不显示新闻信息，
        则复制下面网址，然后复制一个cookie即可，替换掉News.py文件中cookie的值即可
        https://s.weibo.com/
        '''
        title1,link= News.News_Infor(val)
        Infor = zip(link,title1)
        print('sina news',title1)

        # 过滤出包含关键字的文章
        info = Data.objects.filter(title__contains=val)

        ###动态构建图谱数据
        data = []
        for item in info:
            title = item.author
            school = item.school
            workname = item.title
            date = item.date
            data.append((title, school,workname))
        #print(data)
        path = getAuthor_School(data)
        getAuthor(path)
        getTeam(data)
        getCooperation()
        print('tp data')
        ###
        #Paginator分页器 创建分页对象paginator，每页显示20条
        paginator = Paginator(info, 20)
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('index')
        #session获取用户名
        username = request.session.get('username')
        try:
            #插入用户搜索记录
            model = user(username=username, history=val)
            model.save()
        except:
            print(">>>>>>")
            print("浏览记录插入失败")
        try:
            Page = paginator.page(page)

        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            Page = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            Page = paginator.page(paginator.num_pages)
        return render_to_response('result.html',{'username':username,'Infor':Infor,'page':Page,'paginator':paginator,'text':text,'val':val})

#直方图
# def Echarts(request):
#     data = []
#     # 省份发表论文统计
#     for item in Data.objects.filter(title__contains=val):
#         data.append(item.city)

#     sort_data = sorted(dict(Counter(data)).items(), key=lambda x: x[1], reverse=True)[:4]
#     name = [city[item[0]-1] for item in sort_data]
#     key = [{'name':name[i],'value':sort_data[i][1]} for i in range(len(sort_data))]

#     return render_to_response('echarts.html',{'val':val,'key':json.dumps(key),'name':json.dumps(name)})

def Echarts(request):
    data = []
    # 省份发表论文统计
    for item in Data.objects.filter(title__contains=val):
        data.append(item.school)

    # print(dict(Counter(data)).items())
    sort_data = sorted(dict(Counter(data)).items(), key=lambda x: x[1], reverse=True)[:4]
    print(sort_data)
    name = [item[0] for item in sort_data]
    key = [{'name':name[i],'value':sort_data[i][1]} for i in range(len(sort_data))]

    return render_to_response('echarts.html',{'val':val,'key':json.dumps(key),'name':json.dumps(name)})


#发文趋势
# def trend(request):


# def institue(request):


#地图展示
def Chinamap(request):
    #检索内容相关论文数据
    data = [item.city for item in Data.objects.filter(title__contains=val)]

    #包含检索主题的省份id
    has_paper_id = list(dict(Counter(data)).keys())

    #包含检索主题省份的论文数量
    paper_num = list(dict(Counter(data)).values())

    #补全其他省份的论文数量 补0即可
    paper_num = paper_num+[0]*(len(city)-len(paper_num))

    #不包含检索主题的省份id
    not_has_paper_id = [(city.index(item)+1) for item in city if (city.index(item)+1) not in has_paper_id]

    #所有省份id
    all_paper_id = has_paper_id + not_has_paper_id

    #构建地图所需数据
    data = [{'name':city[(all_paper_id[i]-1)],'value':paper_num[i]} for i in range(len(all_paper_id))]

    # 传最大最小值绘制热度
    a = min(paper_num)
    b = max(paper_num)
    return render_to_response('chinamap.html',{'val':val,'data':json.dumps(data),'min':a,'max':b})

#评论入口
def insert(request):
    return render(request,'insert.html')

#翻页
def Page(request):
    if request.method == "GET":
        text = getbdinfo.getBaiDuInfo(val)  
        if(val!=""):
            username = request.session.get('username')
            title1,link = News.News_Infor(val)#新闻爬虫展示
            Infor = zip(link,title1)
            info = Data.objects.filter(title__contains=val)
            paginator = Paginator(info,20)
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1,参数使用问号传递
            page = request.GET.get('index')
            try:
                Page = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                Page = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                Page = paginator.page(paginator.num_pages)
            template_view = 'result.html'
            return render(request, template_view, {'username':username,'Infor': Infor,'paginator':paginator,'page':Page,'text':text,'val':val})
        else:
            return render_to_response('search.html')

# 机构扇形图
def EchartJiGou(request):
    d = []
    # 存储论文来源数据
    for item in Data.objects.filter(title__contains=val):
        d.append(item.name)

    # 统计论文来源频次
    Name = list(dict(Counter(d)).keys())
    counter_value = list(dict(Counter(d)).values())

    #构建统计图的数据
    data = [{'value': counter_value[i],'name':Name[i]} for i in range(len(counter_value))]

    return render_to_response('echarts-jigou.html', {'Name':json.dumps(Name),'data':json.dumps(data),'val':val})

# 右侧扇形图
def Echscirle(request):
    d = []
    # 存储论文来源数据
    for item in Data.objects.filter(title__contains=val):
        d.append(item.name)

    # 统计论文来源频次
    Name = list(dict(Counter(d)).keys())
    counter_value = list(dict(Counter(d)).values())

    #构建统计图的数据
    data = [{'value': counter_value[i],'name':Name[i]} for i in range(len(counter_value))]

    return render_to_response('echarts-cirle.html', {'Name':json.dumps(Name),'data':json.dumps(data),'val':val})

#知识图谱
def Graph(request):
    #获取构建图谱的全部数据
    node,edge = getTpData()
    return render(request,'graph-test.html',{'val':val,'node':json.dumps(node),'edge':json.dumps(edge)})
