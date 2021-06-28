#coding:utf-8
from django.shortcuts import render,redirect,HttpResponse
import hashlib
from login.models import Register

from login.form import UserLogin,UserRegister
from django.http import HttpResponseRedirect#业务逻辑处理完跳转指定网址

# Create your views here.
def take_md5(content):
    hash = hashlib.md5()    #创建hash加密实例
    hash.update(content.encode('utf8'))    #hash加密，必须编码后在加密
    result = hash.hexdigest()  #得到加密结果
    return result

#注册
def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)#绑定表单
        if form.is_valid(): #绑定成功返回True，获取表单信息
            username = form.cleaned_data['username']#获取username key对应的value
            namefilter = Register.objects.filter(username = username)#获取数据库字段信息
            print("-----")
            print(len(namefilter))
            print("-----")
            if len(namefilter) > 0:
                return render(request,'register.html',{'error':'用户名已存在'})
            else:
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    return render(request,'register.html',{'error':'两次输入的密码不一致！'})
                else:
                    #password = take_md5(password1)
                    password = password1#不使用md5加密
                    email = form.cleaned_data['email']
                    phone_number = form.cleaned_data['phone_number']
                    #将表单写入数据库
                    user = Register.objects.create(username=username,password=password,email=email,\
                                                   phone_number=phone_number)
                    user.save()
                    #return render(request,'login.html')
                    #注册完成之后进行登陆页面跳转
                    return HttpResponseRedirect('/login/')
        else:
            form = UserRegister()
            return render(request,'register.html',{'form':form})
    else:
        form = UserRegister()
        return render(request,'register.html',{'form':form})

#登录
def login(request):
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid(): #获取表单信息
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #password = take_md5(password)
            namefilter = Register.objects.filter(username=username,password=password)
            #namefilter 返回的结果 0：失败 1：成功
            print("-----")
            print(len(namefilter))
            print("-----")
            if len(namefilter) > 0:
                request.session['username'] = username
                name = request.session.get('username')
                return render(request,'search.html',{'username':name,'operation':'登录'})
            else:
                return render(request,'login.html',{'error':'用户名或密码错误'})
        else:
            form = UserLogin()
            return render(request, 'login.html', {'form': form})
    else:
        form =UserLogin()
        return render(request,'login.html',{'form':form})
def index(request):
    return render(request,'index3.html')
#个人信息入口
def info(request):
    username = request.session.get('username')
    return render(request,'info.html',{'username':username})
#个人信息修改
def infochange(request):
    if request.method == 'GET':
        return redirect('/info')
    elif request.method == 'POST':
        username = request.session.get('username')
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        #判断账号、密码、邮箱、电话是否为空，若为空，则跳转回修改页面
        if str(uname) == '' or str(password) == '' or str(email) == '' or str(phone) == '':
            return redirect('/info')
        #不为空则进行修改个人信息
        else:
            model = Register.objects.filter(username=username)\
                .update(username=uname,password=password,email=email,phone_number=phone)
            #修改后直接提交
            # jump_to_console = '''<html><body onLoad="window.top.location.href='/'" ></body></html>'''
            # response = HttpResponse(jump_to_console)
            # return response
            #3秒后返回登录页面
            return render(request,'test1.html',{'username':username})
#修改个人信息后重定向到首页
def redict(request):
    '''
    由于个人信息是通过iframe加载的，直接使用重定向redirect会将重定向的内容
    定向到iframe中，展示为嵌套，烦
    通过下面直接定向到正常首页
    '''
    href = '''<html><body onLoad="window.top.location.href='/'" ></body></html>'''
    response = HttpResponse(href)
    return response