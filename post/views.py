from django.shortcuts import render,redirect
from django.core.cache import cache
from post.models import Post
from math import ceil


def create(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		content = request.POST.get('content')
		post = Post.objects.create(title=title, content=content)
		return redirect('/post/read/?post_id=%d'%post.id)
	else:	
		return render(request,'create.html')


def edit(request):
	if request.method == 'POST':
		# 取出原文章
		post_id = request.POST.get('post_id')
		post = Post.objects.get(id=post_id)
		# 修改文章
		post.title = request.POST.get('title')
		post.content = request.POST.get('content')
		post.save()
		# cache.set('post-%s'%post_id, post)  # 修改缓存
		return redirect('/post/read/?post_id=%d' % post.id)
	else:
		# get不修改
		post_id = request.GET.get('post_id')
		post = Post.objects.get(id=post_id)
		return render(request,'edit.html',{'post': post})


def read(request):
	post_id = int(request.GET.get('post_id'))
	try:
		# key = 'post-%d'%post_id
		# post = cache.get(key)
		# print('from get cache %d'%post_id)
		# if post is None:
		post = Post.objects.get(id=post_id)
			# cache.set(key,post)
			# print('from get db %d'%post_id)
		return render(request,'read.html',{'post': post})
	except Post.DoesNotExist:
		return redirect('/post/list/')


def list(request):
	page = int(request.GET.get('page',1)) # 当前页码，默认为-1
	p = 5
	# 计算页数
	total = Post.objects.count()
	pages = ceil(total / p)

	# 取出本页需要实现的文章	
	start = (page - 1) * p
	end = start + 5
	posts = Post.objects.all()[start: end]
	return render(request,'post_list.html', { "posts": posts, 'pages': range(pages) })


def search(request):
	keyword = request.POST.get('keyword')
	posts = Post.objects.filter(content__contains=keyword)
	return render(request,'search.html',{'posts': posts})

