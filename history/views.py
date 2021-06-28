from django.shortcuts import render
from history.models import user
from history.ItemCF import ItemCF
from collections import Counter
from HelloWorld.models import Data
import random

from other.author_school_possess import getAuthor_School
from other.author import getAuthor
from other.team import getTeam
from other.cooperation import getCooperation
from other.tp_data_pro import getTpData
import json
# Create your views here.

#推荐论文功能
def recommend(request):
    #存储搜索关键词 防止基于ItemCF推荐为空与单个用户情况 冷启动问题
    val = request.session.get('val')
    #获取用户搜索历史，过滤出全部记录
    history = user.objects.filter()
    username = request.session.get('username')
    re_data = []
    for item in history:
        #获取历史搜索记录中用户名
        username = item.username
        #用户搜索历史
        his = item.history
        re_data.append(str(username)+','+str(1)+','+str(his))
    print(re_data)
    #调用Counter统计元素出现次数
    con_list = Counter(re_data)
    #print(con_list)
    #可使用Counter处理，
    re_data = list(set(re_data))
    #根据当前登录用户 推荐排名前3的主题方向 调用ItemCF接口
    print(re_data)
    recommedDic = ItemCF(re_data,str(username))
    #存储推荐主题
    val_list = []
    for k,v in recommedDic.items():
        print("推荐主题:"+str(k))
        val_list.append(k)
    #推荐列表不为空
    if len(val_list) != 0:
        #推荐信息存储列表
        recommend_list = []
        #遍历查询不同推荐主题的标题进行展示
        for i in range(len(val_list)):
            data = Data.objects.filter(title__contains=val_list[i])
            for item in data:
                title = item.title
                recommend_list.append(title)
        #选取20条展示，若不足20条论文
        try:
            index = [random.randint(0,len(recommend_list)) for i in range(20)]
            #随机20条进行展示 while循环防止下标重复
            while len(list(set(index))) < 20:
                index = [random.randint(0, len(recommend_list)) for i in range(20)]
            recommend_top20 = []
            for i in index:
                recommend_top20.append(recommend_list[i])
        except:
            index = [random.randint(0, len(recommend_list)) for i in range(10)]
            # 随机5条进行展示
            while len(list(set(index))) < 10:
                index = [random.randint(0, len(recommend_list)) for i in range(10)]
            recommend_top20 = []
            for i in index:
                recommend_top20.append(recommend_list[i])
    #推荐列表为空
    else:
        # 推荐信息存储列表
        recommend_list = []
        #过滤当前用户搜索的关键词处理   可做基于内容的推荐
        data = Data.objects.filter(title__contains=val)
        for item in data:
            title = item.title
            recommend_list.append(title)
        index = [random.randint(0, len(recommend_list)) for i in range(20)]
        while len(list(set(index))) < 20:
            index = [random.randint(0, len(recommend_list)) for i in range(20)]
        recommend_top20 = []
        for i in index:
            recommend_top20.append(recommend_list[i])
    return render(request,'recommend.html',{'data1':recommend_top20,'username':username})

#查看论文详情并显示该论文的图谱
def detail(request):
    #获取前端传送的title参数数据
    title = request.GET.get('title')
    #精确过滤出此文章的信息
    data = Data.objects.filter(title=title)
    for item in data:
        # print(dir(item))
        author = item.author
        school = item.school
        abstract = item.abstract
        title = item.title
        id = item.id
        org = item.name
        date = item.date
    #存储被查看文章的作者信息，每一个作者为一个列表元素
    author_list = author.split(',')
    #存储分别与被查看文章作者有关查找返回的QuerySet集合   模糊查询结果
    query = []
    #存储图谱原始数据
    tp_data = []
    #遍历模糊查询作者，返回与被查找文章作者有关的QuerySet集合
    #author__contains模糊查询，存在字符串嵌套问题，不精确，下方处理
    for a in author_list:
        query.append(Data.objects.filter(author__contains=a))
    #精确保存图谱原始数据 遍历不同作者
    for i in range(len(author_list)):
        #遍历每一个QuerySet对象
        for item in query[i]:
            print(item.title)
            #获取不精确的作者 学校信息  均为组合模式
            a = item.author
            s = item.school
            t = item.title
            #不精确的作者集合处理为列表
            a_list = str(a).split(',')
            #若是被查看文章作者存在于不精确的作者集合中
            if author_list[i] in a_list:
                #将此作者 学校信息（此时为精确）添加到图谱原始数据中
                tp_data.append((a,s,t))

    ###更好的显示图谱 截取少量数据
    try:
        #由于图谱数据过多  切片取部分元素进行展示
        tp_data = tp_data[:6]
        #若是本篇文章作者等信息未存在于图谱初始数据中  则添加  没有信息时也会添加最少包含本篇信息的数据
        if (author,school,title) not in tp_data:
            tp_data.append((author,school,title))
    except:
        #若是没有与被查找文章有关的信息 则将被查找文章信息进行添加，展示图谱 上述if语句间接处理了此条语句的功能
        if len(tp_data) == 0:
            tp_data.append((author,school,title))


    print("精确作者、单位")
    print((author,school))
    print("图谱初始数据(作者、单位)--")
    print(tp_data)
    print("图谱初始数据--")
    #对原始作者 学校进行处理
    path = getAuthor_School(tp_data)
    #构造作者数据
    getAuthor(path)
    #构造团队数据
    getTeam(tp_data)
    #关系构造
    getCooperation()
    #图谱数据构造
    node, edge = getTpData()

    ###处理摘要 规则显示 针对不同类型摘要进行格式化处理
    abstract = abstract.replace(' ','')
    #信息提取
    if '基金：' in abstract and 'DOI：' not in abstract:
        findex = abstract.find('基金')
        zy = abstract[:(findex - 1)].replace(',', '', 1)
        kindex = abstract.find('关键词')
        found = abstract[findex:(kindex - 1)].replace(',', '')
        flindex = abstract.find('分类号')
        keyword = abstract[kindex:(flindex - 1)].replace(',', '')
        return render(request, 'detail1.html', {'node':json.dumps(node),'edge':json.dumps(edge),'title': title, 'author': author, 'school': school, \
                                               'zy': zy, 'found':found,'keyword':keyword,'org': org, 'date': date})
    elif '基金：' in abstract and 'DOI：' in abstract:
        findex = abstract.find('基金')
        zy = abstract[:(findex - 1)].replace(',', '', 1)
        kindex = abstract.find('关键词')
        found = abstract[findex:(kindex - 1)].replace(',', '')
        dindex = abstract.find('DOI')
        keyword = abstract[kindex:(dindex - 1)].replace(',', '')
        return render(request, 'detail1.html', {'node':json.dumps(node),'edge':json.dumps(edge),'title': title, 'author': author, 'school': school, \
                                                'zy': zy, 'found': found, 'keyword': keyword, 'org': org, 'date': date})
    elif 'DOI：' not in abstract:
        kindex = abstract.find('关键词')
        zy = abstract[:(kindex - 1)].replace(',', '', 1)
        flindex = abstract.find('分类号')
        keyword = abstract[kindex:(flindex - 1)].replace(',', '')
        return render(request, 'detail.html', {'node':json.dumps(node),'edge':json.dumps(edge),'title': title, 'author': author, 'school': school, \
                                                'zy': zy, 'keyword': keyword, 'org': org, 'date': date})
    else:
        kindex = abstract.find('关键词')
        zy = abstract[:(kindex - 1)].replace(',', '', 1)
        dindex = abstract.find('DOI')
        keyword = abstract[kindex:(dindex - 1)].replace(',', '')
        return render(request,'detail.html',{'node':json.dumps(node),'edge':json.dumps(edge),'title':title,'author':author,'school':school,\
                                         'zy': zy, 'keyword': keyword,'org':org,'date':date})

#查看论文功能 预留功能
def dfind(request):
    return render(request,'dfind.html')
def testfind(request):
    title = request.GET.get('title')
    return render(request,'testfind.html',{'title':title})
def find(request):
    title = request.GET.get('title')
    data = Data.objects.filter(title=title)
    for item in data:
        author = item.author
        school = item.school
        abstract = item.abstract
        id = item.id
        org = item.name
        date = item.date
    abstract = abstract.replace(' ', '')
    # 信息提取
    if '基金：' in abstract and 'DOI：' not in abstract:
        findex = abstract.find('基金')
        zy = abstract[:(findex - 1)].replace(',', '', 1)
        kindex = abstract.find('关键词')
        found = abstract[findex:(kindex - 1)].replace(',', '')
        flindex = abstract.find('分类号')
        keyword = abstract[kindex:(flindex - 1)].replace(',', '')
        return render(request, 'find2.html',{'title': title, 'author': author,'school': school, \
                       'zy': zy, 'found': found, 'keyword': keyword, 'org': org, 'date': date})
    elif '基金：' in abstract and 'DOI：' in abstract:
        findex = abstract.find('基金')
        zy = abstract[:(findex - 1)].replace(',', '', 1)
        kindex = abstract.find('关键词')
        found = abstract[findex:(kindex - 1)].replace(',', '')
        dindex = abstract.find('DOI')
        keyword = abstract[kindex:(dindex - 1)].replace(',', '')
        return render(request, 'find2.html',{'title': title, 'author': author,'school': school, \
                       'zy': zy, 'found': found, 'keyword': keyword, 'org': org, 'date': date})
    elif 'DOI：' not in abstract:
        kindex = abstract.find('关键词')
        zy = abstract[:(kindex - 1)].replace(',', '', 1)
        flindex = abstract.find('分类号')
        keyword = abstract[kindex:(flindex - 1)].replace(',', '')
        return render(request, 'find1.html',{'title': title, 'author': author,'school': school, \
                       'zy': zy, 'keyword': keyword, 'org': org, 'date': date})
    else:
        kindex = abstract.find('关键词')
        zy = abstract[:(kindex - 1)].replace(',', '', 1)
        dindex = abstract.find('DOI')
        keyword = abstract[kindex:(dindex - 1)].replace(',', '')
        return render(request, 'find1.html',{'title': title, 'author': author,'school': school, \
                       'zy': zy, 'keyword': keyword, 'org': org, 'date': date})