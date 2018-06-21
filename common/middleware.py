from django.utils.deprecation import MiddlewareMixin
import time

class BlockMiddleware(MiddlewareMixin):
	'''限制用户的访问频率最大为每秒2次，超过两次时，睡一会儿'''
	
	def process_request(self, request):
		current = time.time()
		request_time = request.session.get('request_time', [0, 0])
		if (current - request_time[0]) < 1:
			time.sleep(5)
			current = time.time()
		request.session['request_time'] = [request_time[1], current]
	
	