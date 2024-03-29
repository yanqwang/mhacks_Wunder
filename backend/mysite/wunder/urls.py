from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'css', views.get_css, name='get_css'),
	url(r'images', views.get_image, name='get_image'),
	url(r'search', views.get_search, name='search'),
	url(r'it', views.upload_recv, name='upload_recv'),
	url(r'upload', views.get_upload, name='upload'),
	url(r'your-name', views.search_recv, name='search_recv'),

]