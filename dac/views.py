from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from dac.models import Beer
from registration.backends.simple.views import RegistrationView


# General site pages
def index(request):
	context_dict = {"beers":None,"pubs":None}
	#get database stuff

	beers = Beer.objects.all()
	context_dict["beers"] = beers

	return render(request, 'dac/index.html', context=context_dict)

def sitemap(request):
	return HttpResponse("A sitemap")


#beer stuff
def beers(request,beer_slug=None):
	context_dict = {'beer': None,}


	
	#render beer_list.html saves trouble with multi purpose page
	#could use template tags as singular beer will be reapeated
	if not beer_slug:
		return HttpResponse("where beers will be listed")

	#an explicit beer slug has been passed so just get that beer specifically
	beer = get_object_or_404(Beer,slug=beer_slug)
	print(beer.image)
	context_dict["beer"] = beer
	context_dict["single"] = True


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

class UserRegistrationView(RegistrationView):


	# def get_success_url(self, user):
	# 	'''send the user to setup their accounts other features'''
	# 	print("redirect called")
	# 	return "/account"

	def register(self,form):
		print("register called")
		user = form.save()
		user.set_password(user.password)
		user.save()
		#spicy autologin
		username = self.request.POST['username']
		password = self.request.POST['password1']
		#auth_user = authenticate(username=username, password=password)
		auth_login(self.request,user)


@login_required
def user_details(request):
	return HttpResponse("what a meme")

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
