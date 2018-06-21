from django.shortcuts import render,redirect

from django.core.cache import cache
from post.helper import page_cache
from post.models import Comment
from post.models import Post

from math import ceil
from post.helper import read_count
from post.helper import get_top_n
from post.helper import is_login


# 创建文章
@is_login
def create(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		content = request.POST.get('content')
		uid = request.session.get('uid')
		post = Post.objects.create(uid=uid,title=title, content=content)
		return redirect('/post/read/?post_id=%d'%post.id)
	else:
		return render(request,'create.html')


# 修改文章
@is_login
def edit(request):
	if request.method == 'POST':
		# 取出原文章
		post_id = request.POST.get('post_id')
		post = Post.objects.get(id=post_id)
		# 修改文章
		post.title = request.POST.get('title')
		post.content = request.POST.get('content')
		post.save()
		tags = request.POST.get('tags', '')
		tag_names = [w.strip().title()
					for w in tags.replace('，',',').split(',')
					if w.strip()]
		post.update_tags(tag_names)
		# cache.set('post-%s'%post_id, post)  # 修改缓存
		
		return redirect('/post/read/?post_id=%d' % post.id)
	else:
		# get不修改
		post_id = request.GET.get('post_id')
		post = Post.objects.get(id=post_id)
		tag_str = ','.join([t.name for t in post.tags])
		return render(request,'edit.html',{'post': post,'tag_str':tag_str})


# @read_count记录文章阅读次数
# @page_cache(300)将文章存入redis 
@read_count
@page_cache(3)
def read(request):
	post_id = int(request.GET.get('post_id',-1))
	try:
		# 存入缓存
		# key = 'post-%d'%post_id
		# post = cache.get(key)
		# print('from get cache %d'%post_id)
		# if post is None:
			# post = Post.objects.get(id=post_id)
			# cache.set(key,post)
			# print('from get db %d'%post_id)

		post = Post.objects.get(id=post_id)
		return render(request,'read.html',{'post': post})
	except Post.DoesNotExist:
		return redirect('/user/login/')


# 显示文章
# @page_cache(300) 将view的list函数存入Redis
@page_cache(300)
def list(request):
	page = int(request.GET.get('page',1)) # 当前页码，默认为-1
	p = 5
	# 计算页数
	total = Post.objects.count()
	pages = ceil(total / p)

	# 取出本页需要实现的文章	
	start = (page - 1) * p
	end = start + 5
	posts = Post.objects.all().order_by('-created')[start: end]
	return render(request,'post_list.html', { "posts": posts, 'pages': range(pages) })


# 搜索文章
def search(request):
	keyword = request.POST.get('keyword')
	posts = Post.objects.filter(content__contains=keyword)
	return render(request,'search.html',{'posts': posts})


# 对阅读量前十的进行排序
def top10(request):
	rank_data = get_top_n(10)
	return render(request,'top10.html', {'rank_data': rank_data})


@is_login
def commont(request):
	uid = request.session.get('uid')
	post_id = request.POST.get('post_id')
	content = request.POST.get('content')	
	post = Comment.objects.create(uid=uid,post_id=post_id,content=content)
	return redirect('/post/read/?post_id=%s' % post_id)