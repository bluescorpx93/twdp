from django.conf.urls import url
from rango import views

urlpatterns=	[ 
	url(r'^$', views.index, name='index'), 
	url(r'^category/(\d+)/$', views.category, name='category'),
	url(r'^add_category/$', views.add_category, name='add_category'),
	url(r'^category/(\d+)/add_page/$', views.add_page, name='add_page'),
	url(r'^about/$', views.about, name='about'),
	# url(r'^search/$', views.search, name='search'), 
	url(r'^page/(\d+)/$', views.page, name='page_url'), 
	url(r'^like_category/$', views.like_category, name='like_category'),
	url(r'^suggest_category/$', views.suggest_category, name='suggest_category'), 
	url(r'^auto_add_page/$', views.auto_add_page, name='auto_add_page')
	


	]