from django.shortcuts import render, redirect
from django.http import HttpResponse

def root_page(request):
	return render(request, 'root-home.html')