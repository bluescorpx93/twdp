"""twdp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rango import urls
from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
	def get_success_url(self,request, user):
		return '/rango/'

# Problem here, cant load form, because cant find WHICH View to import
# class MyPasswordChangeView(RegistrationView):
# 	def get_success_url(request):
# 		return '/rango/'

urlpatterns =	[
	url(r'^admin/', include(admin.site.urls)),
	url(r'^rango/', include(urls)), 
	url(r'^accounts/', include('registration.backends.simple.urls')),
	url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'), 
	# url(r'^password/$', include('registration.backends.simple.urls')), 
	# url(r'^password/change/$', MyPasswordChangeView.as_view(), name='auth_password_change'), 
	]