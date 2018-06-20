from django.core.cache import cache
from post.models import Post
from common import rds
from common import keys

def page_cache(times):
	def wrap1(view_func):
		def wrap2(request):
			# key的构造: view /vars /user
			key = keys.PAGE_CACHE_KEY %(request.session.session_key,request.get_full_path())
			res = cache.get(key)
			print('获取-------%s'%res)

			if res is None:  				# 检查缓存中是否有结果
				res = view_func(request)  	# 如果没有，直接执行原函数
				cache.set(key,res,times)
				print('设置--------%s'%res)

			return res  					# 如果有，直接返回缓存response
		return wrap2
	return wrap1


def read_count(read_view):
	def wrap(request):
		res = read_view(request)
		if res.status_code < 300:
			post_id = request.GET.get('post_id')
			print(post_id)
			rds.zincrby(keys.READ_RANk_KEY, post_id)
		return res
	return wrap


def get_top_n(num):
	ori_data = rds.zrevrange(b'ReadRank', 0, num - 1, withscores=True)  
	rank_data = [[int(post_id), int(count)] for post_id, count in ori_data]
	
	# 批量获取post对象
	post_id_list = [post_id for post_id, _ in rank_data]
	posts = Post.objects.filter(id__in=post_id_list)
	posts = sorted(posts,key=lambda p: post_id_list.index(p.id))

	for item, post in zip(rank_data,posts):
		item[0] = post
	return rank_data
