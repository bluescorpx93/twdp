from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from datetime import datetime
from rango.bing_search import run_query
from django.contrib.auth.decorators import login_required

def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	page_list     = Page.objects.order_by('-views')[:5]
	context_dict  = {'categories': category_list, 'pages': page_list}
	visits        = request.session.get('visits')
	 
	if not visits:
		visits = 1

	reset_last_visit_time = False
	last_visit            = request.session.get('last_visit')

	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		if (datetime.now() - last_visit_time).seconds > 0:
			visits = visits + 1
			reset_last_visit_time = True
	else:
		reset_last_visit_time = True

	if reset_last_visit_time:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits

	context_dict['visits'] = visits
	response = render(request,'rango/index.html', context_dict)

	return response


def category(request, cat_id):
	context_dict = {}
	context_dict['result_list']=	None
	context_dict['query']=	 None
	try:
		category                      = Category.objects.get(id=cat_id)
		pages                         = Page.objects.filter(category=category).order_by('-views')
		context_dict['category_name'] = category.name
		context_dict['pages']         = pages
		context_dict['category']      = category
		context_dict['cat_id']        = cat_id
	except Category.DoesNotExist:
		pass
	if request.method=='POST':
		query=	request.POST['query'].strip()
		if query:
			result_list=	run_query(query)
			context_dict['result_list']=	result_list
			context_dict['query']=	query
		if not context_dict['query']:
			context_dict['query']=	category.name
	# if request.method == 'GET':
	return render(request, 'rango/category.html', context_dict)

from rango.forms import CategoryForm

def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()
	return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, cat_id):
	try:
		cat = Category.objects.get(id=cat_id)
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request, cat_id)
		else:
			print form.errors
	else:
		form = PageForm()

	context_dict = {'form':form, 'category': cat, 'cat_id': cat_id,}

	return render(request, 'rango/add_page.html', context_dict)

def about (request):
	return render(request, 'rango/about.html', {})

def search(request):
	result_list=	[]
	if request.method=='POST':
		query=	request.POST['query'].strip()
		if query:
			result_list=run_query(query)
	return render(request, 'rango/search.html', {'result_list': result_list})

def page(request, page_id):
	page=	Page.objects.get(id=page_id)
	page.views=	page.views+1
	page.save()
	# page_id = 1
	# page = None
	# url=	'/rango/'
	# if request.method== 'GET':
	# 	if page_id in request.GET:
	# 		page_id=	request.GET['page_id']
	# 		try:
	# 			page=	Page.objects.get(id=page_id)
	# 			page.views=	page.views+1
	# 			page.save()
	# 			url='/rango/'+request.GET['page_id']
	# 		except:
	# 			pass
	return render(request, 'rango/page.html', {'page': page})

@login_required
def like_category(request):

	 cat_id = None
	 if request.method == 'GET':
		  cat_id = request.GET['category_id']

	 likes = 0
	 if cat_id:
		  cat = Category.objects.get(id=int(cat_id))
		  if cat:
				likes = cat.likes + 1
				cat.likes =  likes
				cat.save()

	 return HttpResponse(likes)

def get_category_list(max_results=0, starts_with=''):
	cat_list=[]
	if starts_with:
		cat_list=	Category.objects.filter(name__istartwith=starts_with)
	if max_results>0:
		if cat_list.count() > max_results:
			cat_list=	cat_list[:max_results]
	return cat_list

def suggest_category(request):
	cat_list=	[]	
	starts_with=''
	if request.method=='GET':
		starts_with=	request.GET['suggestion']
	cat_list=	get_category_list(7, starts_with)
	return render(request, 'rango/category.html', cat_list)

@login_required
def auto_add_page(request):
  cat_id = None
  url = None
  title = None
  context_dict = {}
  if request.method == 'GET':
      cat_id = request.GET['category_id']
      url = request.GET['url']
      title = request.GET['title']
      if cat_id:
          category = Category.objects.get(id=int(cat_id))
          p = Page.objects.get_or_create(category=category, title=title, url=url)

          pages = Page.objects.filter(category=category).order_by('-views')

          # Adds our results list to the template context under name pages.
          context_dict['pages'] = pages

  return render(request, 'rango/page_list.html', context_dict)