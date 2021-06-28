from django.shortcuts import render
from review.models import Submit
# Create your views here.
#评论提交后的业务逻辑
def submit(request):
    #获取用户名
    username = request.session.get('username')
    #获取表单传的数据
    if request.method == 'POST':
        qq = request.POST.get('q')
        review = request.POST.get('r')
    try:
        model = Submit(username=username,qq=qq,review=review)
        model.save()
    except:
        print(">>>>>")
        print("connection failed")
    #存储数据库中
    return render(request,'test.html',{'username':username})
