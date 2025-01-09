# coding:utf-8
from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from .forms import LoginForm
import json


# 用户注册
def do_register(request):
    try:
        msg = ""
        if request.method == "GET":
            return render(request, "register.html", locals())

        if request.method == "POST":
            # 从请求中获取用户输入
            username = request.POST.get("username", '')
            mobile = request.POST.get("mobile", '')
            email = request.POST.get("email", '')
            password = request.POST.get("password", '')
            password2 = request.POST.get("password2", '')

            dict1 = {
                'username': username,
                'mobile': mobile,
                'email': email,
                'password': password,
                'password2': password2
            }

            # 验证输入
            if not username:
                msg = "用户名不能为空"
            elif not mobile:
                msg = "手机号不能为空"
            elif not email:
                msg = "email不能为空"
            elif len(username) < 6 or len(password) < 6 or len(password2) < 6:
                msg = "账号和密码必须大于6位"
            elif password != password2:
                msg = "两次输入的密码不一致"
            elif len(mobile) != 11:
                msg = "手机号必须为11位且格式正确"
            elif UserProfile.objects.filter(username=username).exists():
                msg = "用户名已经存在"

            # 如果存在错误信息，返回注册页面
            if msg:
                return render(request, "register.html", context={'msg': msg, 'dict1': dict1})

            # 创建新用户
            new_user = UserProfile(
                username=username,
                mobile=mobile,
                email=email,
                mpassword=password  # 使用简单明文，后续建议采用安全的加密存储方式
            )
            new_user.set_password(password)  # 设置加密密码
            new_user.save()  # 保存到数据库

            # 注册成功后重定向到登录页面
            return redirect("accounts:login")

    except Exception as e:
        print(e)  # 打印错误信息
        msg = "添加失败，系统错误"

    return render(request, "register.html", context={'msg': msg, 'dict1': ''})


# 用户登录
def user_login(request):
    try:
        if request.user.is_authenticated:  # 如果用户已登录，重定向到首页
            return redirect("/")

        if request.method == 'POST':
            login_form = LoginForm(request.POST)  # 获取登录表单数据

            if login_form.is_valid():  # 如果表单有效
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]

                # 验证用户身份
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)  # 登录用户
                    return redirect("/")  # 登录成功，重定向主页
                else:
                    errorinfo = "账号或密码不正确"
            else:
                errorinfo = "账号或密码格式错误"

            return render(request, 'login.html', {'login_form': login_form, "errorinfo": errorinfo})

        else:
            login_form = LoginForm()  # 显示空登录表单
            return render(request, 'login.html', {'login_form': login_form})

    except Exception as e:
        print(e)  # 打印错误信息
        errorinfo = "系统错误"
        return render(request, 'login.html', {'login_form': LoginForm(), "errorinfo": errorinfo})


# 用户退出
@login_required
def user_logout(request):
    try:
        logout(request)  # 退出登录
        return redirect('accounts:login')
    except Exception as e:
        print(e)  # 打印错误信息
    return render(request, "error.html", {"msg": "退出错误"})


# 我的信息页面
@login_required
def my_info(request):
    try:
        user = request.user
        if request.method == "GET":
            return render(request, "my_info.html", locals())

        if request.method == "POST":
            # 获取用户提交的信息
            username = request.POST.get("username", "")
            mobile = request.POST.get("mobile", "")
            email = request.POST.get("email", "")
            password = request.POST.get("password", "123456")

            # 处理用户上传的头像
            input_img = request.FILES.get('input_img', None)

            # 验证输入
            if not username or len(username) < 6:
                msg = "用户名不能为空，必须大于6位"
            elif not mobile or len(mobile) != 11:
                msg = "手机号不能为空，必须11位且格式正确"
            else:
                user.username = username
                user.mobile = mobile
                user.email = email
                if input_img:  # 如果上传了图片，更新头像
                    user.header_image = input_img

                user.set_password(password)  # 更新加密密码
                user.save()  # 保存更改
                msg = "修改成功"

            return render(request, "my_info.html", locals())

    except Exception as e:
        print(e)  # 打印错误信息
        msg = "系统错误"

    return render(request, "my_info.html", locals())


# 修改密码
@login_required
def modify(request):
    try:
        user = request.user
        if request.method == 'POST':
            old_password = request.POST.get("oldpassword")
            new_password = request.POST.get("newpassword")
            confirm_password = request.POST.get("conpassword")

            # 验证旧密码
            if not user.check_password(old_password):
                errorinfo = "旧密码错误"
            elif new_password != confirm_password:
                errorinfo = "新密码与确认密码不一致"
            elif len(new_password) < 6:
                errorinfo = "新密码必须大于6位"
            else:
                user.set_password(new_password)  # 设置新密码
                user.save()  # 保存用户
                logout(request)  # 退出用户
                return redirect("/accounts/login")  # 重定向到登录页面

            return render(request, 'modify.html', locals())

        return render(request, 'modify.html', locals())

    except Exception as e:
        print(e)  # 打印错误信息
        errorinfo = "系统错误"

    return render(request, 'modify.html', locals())
