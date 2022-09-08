# 自定义中间件类 执行登录判断
from django.shortcuts import redirect
from django.urls import reverse
import re


class MusicMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("MusicMiddleware")

    def __call__(self, request):
        path = request.path
        print("urls:",path)

        # 判断管理后台是否登录
        urllist = ['/myadmin/login','/myadmin/dologin','/myadmin/logout','/myadmin/verificationcode']

        # 判断当前请求url地址是否以/myadmin开头
        if re.match(r'^/myadmin',path) and (path not in urllist):
            #判断是否登录
            if 'adminuser' not in request.session:
                return redirect(reverse("myadmin_login"))

        response = self.get_response(request)

        return response
