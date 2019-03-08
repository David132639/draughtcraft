from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# General site pages
def index(request):
	context_dict = {}
	return render(request, 'dac/index.html', context=context_dict)

def sitemap(request):
	return HttpResponse("A sitemap")


#beer stuff
def beers(request,beer_slug=None):
	context_dict = {'beer_name': beer_slug, }

	if not beer_slug:
		return HttpResponse("where beers will be listed")

	return render(request,'dac/beer.html',context_dict)

def add_beer_review(request,beer_slug):
	#basic form for user adding review to a specific beer
	return HttpResponse("not implemented")
	pass


def beers_reviews(request,beer_slug):
	context_dict = {}
	#get the reviews associated with the beer and return the stuff
	#use same template as pub reviews
	return HttpResponse("not implemented")


#pub stuff

def pubs(request,pub_slug=None):
	context_dict = {}

	if not pub_slug:
		return HttpResponse("print a whole load of pubs")
	return HttpResponse("a specific pub"+pub_slug)

def pubs_beers(request,pub_slug):
	#return a list of the beers that the pub stocks
	return HttpResponse("not implemented")


def pub_reviews(request,pub_slug):
	context_dict = {}

	#get the reviews associated with the pub and return
	#use same template as pub reviews
	return HttpResponse("not implemented yet")


def about(request):
	return render(request,'dac/about.html')

#searching stuff

def search(request):
	HttpResponse("not implemented")
	pass

#account functionality

@login_required
def user_reviews(request):
	context_dict = {}
	HttpResponse("not implemented")
	pass

def login(request):
	HttpResponse("not implemented")
	pass

@login_required
def logout(request):
	HttpResponse("not implemented")
	pass

def register(request):
	HttpResponse("not implemented")
	pass

def restricted(request):
	HttpResponse("Access Restricted")
	pass
