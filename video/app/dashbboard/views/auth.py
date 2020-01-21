from django.views.generic import View
from app.libs.base_render import render_to_response
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.paginator import Paginator  # 分页系统
from app.utils.utils import dashboard_auth


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))
        to = request.GET.get('to','')
        data = {'error': '','to': to}
        # return render_to_response(request, self.TEMPLATE, data)
        return render(request, self.TEMPLATE, data)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        to = request.GET.get('to','')
        data = {'error': ''}

        exists = User.objects.filter(username=username).exists()
        if not exists:
            data['error'] = '不存在该用户'
            return render_to_response(request, self.TEMPLATE, data)
        user = authenticate(username=username, password=password)
        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATE, data)
        if not user.is_superuser:
            data['error'] = '你无权访问'
            return render_to_response(request, self.TEMPLATE, data)

        login(request, user)
        if to:
            return redirect(to)
        return redirect(reverse('dashboard_index'))


class Admin_Manage(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        users = User.objects.all()
        # 分页系统
        page = request.GET.get('page', 1)
        p = Paginator(users, 2)
        total_page = p.num_pages  # 总的页数
        if int(page) <= 1:
            page = 1
        current_page = p.get_page(int(page)).object_list
        data = {'users': current_page, 'total': total_page, 'page_num': int(page)}
        return render_to_response(request, self.TEMPLATE, data)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('dashboard_login'))


class UpdateAdminStatus(View):
    def get(self, request):
        status = request.GET.get('status', 'on')
        _status = True if status == 'on' else False
        request.user.is_superuser = _status
        request.user.save()
        return redirect(reverse('admin'))
