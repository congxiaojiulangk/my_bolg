from django.shortcuts import render,redirect
from post.models import Post
from django.core.cache import cache
from post.views import read


def page_cache(view_func):
	def wrap(request):
		# key的构造: view /vars /user
		key = 'PageCache-%s-%s'%(request.session.session_key,request.get_full_path())
		print('key%s'%key)
		res = cache.get(key)

		# 检查缓存中是否有结果
		if res is None:
			# 如果没有，直接执行原函数
			res = view_func(request)
			cache.set(key,res)
		# 如果有，直接返回缓存response
		return res
	return wrap

