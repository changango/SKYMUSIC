import datetime as datetime
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

from myadmin.models import users


# Create your views here.


from skymusic.settings import BASE_DIR


# 头像上传函数
def upload_img(request, file):
    if request.method == 'POST':
        obj = request.FILES.get(file)
    if not obj:
        return 0
    filepath = '/static/users-images/' + obj.name
    s = os.path.join(BASE_DIR, 'static', 'users-images', obj.name)
    f = open(s, 'wb')
    for chunk in obj.chunks():  # 分片写入
        f.write(chunk)
    context = {'imgpath': filepath}
    return context

# 用户管理
def index(request, pindex=1):
    umod = users.objects.all().order_by('users_id')
    ulist = umod.all()

    mywhere = []
    kw = request.GET.get("key", None)
    if kw:
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append('key=' + kw)

    # 分页处理
    pindex = int(pindex)
    page = Paginator(ulist, 5)
    maxpages = page.num_pages
    #判断当前页面是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list1 = page.page(pindex) #获取当前页数据
    plist = page.page_range #获取页码列表信息

    context = {'userlist': list1, 'plist': plist, 'pindex': pindex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, 'myadmin/user/index.html', context)


def add(request):
    return render(request, 'myadmin/user/add.html')


def insert(request):
    try:
        x = request.POST['password']
        y = request.POST['repassword']

        if x == y:
            ob = users()
            ob.username = request.POST['username']
            ob.nickname = request.POST['nickname']

            pic = upload_img(request,'headprotrait')
            ob.headprotrait = pic['imgpath']
            ob.is_status = 'offline'

            # 将密码做MD5处理
            import hashlib,random
            md5 = hashlib.md5()
            n = random.randint(100000,999999)
            x = x+str(n) # 从表单中获取密码并添加干扰值
            md5.update(x.encode('utf-8')) # 将要产生md5的子串放进去
            ob.password_hash = md5.hexdigest() # 获取md5值
            ob.password_salt = n

            ob.sex = request.POST['sex']
            ob.status = request.POST['status']
            ob.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ob.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ob.save()
            context = {'info': "添加成功！"}
        else:
            context = {'info':"两次密码不一样！"}
    except Exception as error:
        print(error)
        context = {'info': "添加失败！"}
    return render(request, "myadmin/info.html", context)


def delete(request, uid=0):
    try:
        id = request
        ob = users.objects.filter(users_id=uid).delete()
        context = {'info': "删除成功！"}
    except Exception as error:
        print(error)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, uid=0):
    try:
        ob = users.objects.get(users_id=uid)
        context = {'user': ob}
        return render(request, 'myadmin/user/edit.html', context)
    except Exception as error:
        print(error)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, 'myadmin/info.html', context)


def update(request, uid=0):
    try:
        ob = users.objects.get(users_id=uid)
        ob.nickname = request.POST['nickname']

        # 头像信息修改
        pic = upload_img(request, 'headprotrait')
        if pic:
            ob.headprotrait = pic['imgpath']

        ob.status = request.POST['status']
        ob.sex = request.POST['sex']
        ob.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': '修改成功！'}
    except Exception as error:
        print(error)
        context = {'info': '修改失败！'}
    return render(request, 'myadmin/info.html', context)




