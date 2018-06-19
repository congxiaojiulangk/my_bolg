from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from post import views as post_views
from user import views as user_views


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
	url(r'^post/list/',post_views.list, name='list'),
	url(r'^post/create',post_views.create, name='create'),
	url(r'^post/edit/',post_views.edit, name='edit'),
	url(r'^post/read/',post_views.read, name='read'),
	url(r'^post/search/',post_views.search, name='search'),


	url(r'^user/register/', user_views.register, name="register"),	
	url(r'^user/login/', user_views.login, name="login"),
	url(r'^user/info/', user_views.info, name="info"),
	url(r'^user/logout/', user_views.logout, name="logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)