from django.conf.urls import url
from post import views as post_views


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
	url(r'^post/list/',post_views.list, name='list'),
	url(r'^post/create',post_views.create, name='create'),
	url(r'^post/edit/',post_views.edit, name='edit'),
	url(r'^post/read/',post_views.read, name='read'),
	url(r'^post/search/',post_views.search, name='search'),
]
