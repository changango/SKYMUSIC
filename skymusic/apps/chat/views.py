from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from index.models import users, friends


def chat(request):
    return render(request, 'chat/chat.html')


def usersearch(request, pindex=1):
    umod = users.objects.all().order_by('users_id')
    ulist = umod.all()

    mywhere = []
    kw = request.GET.get("key", None)
    if kw:
        mymusic_id = request.session.get('musicuser', [])
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw)).exclude(users_id=mymusic_id['users_id']).values()
        user_min = friends.objects.filter(Q(Q(friend_user1_id=mymusic_id['users_id']) & Q(friend_user1_status=1)) |
                                          (Q(friend_user2_id=mymusic_id['users_id']) & Q(friend_user2_status=1)))
        print(user_min)
        for i in ulist:
            for j in user_min:
                if j.friend_user1.users_id == i['users_id'] or j.friend_user2.users_id == i['users_id']:
                    i['user_status'] = 1

        mywhere.append('key=' + kw)

        # 分页处理
        pindex = int(pindex)
        page = Paginator(ulist, 5)
        maxpages = page.num_pages
        # 判断当前页面是否越界
        if pindex > maxpages:
            pindex = maxpages
        if pindex < 1:
            pindex = 1
        userlist = page.page(pindex)  # 获取当前页数据
        plist = page.page_range  # 获取页码列表信息
    return render(request, 'chat/friend_info.html', locals())


def add_user_friend(request, uid):
    if request.method == 'POST':
        print(request.POST['users_id'])
        user1 = users.objects.get(users_id=uid)
        user2 = users.objects.get(users_id=request.POST['users_id'])
        try:
            ob = friends.objects.get(Q(Q(friend_user1_id=user1.users_id) & Q(friend_user2_id=user2.users_id)) |
                                     (Q(friend_user2_id=user1.users_id) & Q(friend_user1_id=user2.users_id)))
            if ob.friend_user1 == user1:
                ob.friend_user1_status = 1
            elif ob.friend_user2 == user1:
                ob.friend_user2_status = 1
            ob.save()
        except Exception as error:
            ob = friends()
            ob.friend_user1 = user1
            ob.friend_user1_status = 1
            ob.friend_user2 = user2
            ob.save()
    return JsonResponse({"status": "成功关注"})
