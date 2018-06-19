from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password,check_password
from user.forms import UserForm
from user.models import User



def register(request):
	request.session.flush()
	if request.method == 'POST':
		form = UserForm(request.POST, request.FILES)

		if form.is_valid():
			# 创建用户
			user = form.save(commit=False)  # 包含图片保存，用户创建
			user.password = make_password(user.password)  # 加密处理
			user.save()
			# 保持状态
			request.session['uid'] = user.id
			request.session['nickname'] = user.nickname
			return redirect('/user/info/')
		else:
			# return Jsonresponse(forms.errors)
			return render(request, 'register.html',{'error': form.errors})

	else:

		return render(request, 'register.html')


def login(request):

	if request.method == 'POST':
		nickname = request.POST.get('nickname')
		password = request.POST.get('password')
		try:
			user = User.objects.get(nickname=nickname)
		except User.DoesNotExist:
			return render(request,'login.html',{'error':'用户名错误'})

		if check_password(password,user.password):
			request.session['uid'] = user.id
			request.session['nickname'] = user.nickname
			return redirect('/user/info/')
		else:
			return render(request, 'login.html', {'error': '密码错误'})
	else:
		return render(request, 'login.html')


def info(request):
	try:
		uid = request.session.get('uid', '-1')
		user = User.objects.get(id=uid)
	except User.DoesNotExist:
		return redirect('/user/login/')
	return render(request, 'user_info.html', {'user': user})


def logout(request):
	request.session.flush()
	return render(request, 'login.html')