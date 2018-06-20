from post.models import Post
from django.shortcuts import render,redirect
from django.shortcuts import render,redirect

from django.core.cache import cache


def page_cache(times):
	def wrap1(view_func):
		def wrap2(request):
			# key的构造: view /vars /user
			key = 'PageCache-%s-%s'%(request.session.session_key,request.get_full_path())
			res = cache.get(key)
			print('获取-------%s'%res)

			if res is None:  				# 检查缓存中是否有结果
				res = view_func(request)  	# 如果没有，直接执行原函数
				cache.set(key,res,times)
				print('设置--------%s'%res)
				
			return res  					# 如果有，直接返回缓存response
		return wrap2
	return wrap1
