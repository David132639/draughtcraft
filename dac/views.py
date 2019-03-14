from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from dac.models import Beer, Business,UserProfile
from dac.forms import UserProfileForm, BusinessForm
from registration.backends.simple.views import RegistrationView


# General site pages
def index(request):
	context_dict = {"beers":None,"business":None}

	#get top three rated beers but not implemented yet
	beers = Beer.objects.all()[:3]
	business = Business.objects.all()[:3]
	context_dict["business"] = business
	context_dict["beers"] = beers

	return render(request, 'dac/index.html', context=context_dict)

def sitemap(request):
	return HttpResponse("A sitemap")


#beer stuff
def beers(request,beer_slug=None):
	context_dict = {'beer': None,}

	if not beer_slug:
		context_dict['beers'] = Beer.objects.all()
		return render(request,'dac/beer_list.html',context_dict)

	#an explicit beer slug has been passed so just get that beer specifically
	beer = get_object_or_404(Beer,slug=beer_slug)
	context_dict["beer"] = beer

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


#account entrypoint
class UserRegistrationView(RegistrationView):
	def get_success_url(self, user):
		'''send the user to setup their accounts other features'''
		
		return reverse('user_details')

	def register(self,form):
		user = form.save(commit=False)
		#set user attributes/roles
		user.is_business = form.cleaned_data['is_business']
		user.set_password(user.password)
		user.save()
		#spicy autologin
		username = self.request.POST['username']
		password = self.request.POST['password1']
		auth_login(self.request,user)


@login_required
def user_details(request):
	#user account creaton stuff
	profile = UserProfile.objects.get_or_create(user=request.user)[0]
	profile_form = UserProfileForm({'avatar':profile.avatar})
	context_dict = {"profile_form":profile_form}
	if request.user.is_business:
		if not hasattr(profile,'business'):
			business = Business.objects.create(name=request.user.username+"s business",owner=profile)
		else:
			business = profile.business
		business_form = BusinessForm({'name':business.name,'address':business.address,'description':business.description})
		context_dict['business_form'] = business_form
	
	if request.method == 'POST':
		profile_form = UserProfileForm(request.POST, request.FILES,instance=profile)
		if profile_form.is_valid():
			profile_form.save(commit=True)
			return index(request)
		else:
			print(profile_form.errors)

		if request.user.is_business:
			business_form = BusinessForm(request.POST, request.FILES,instance=business)
			if business_form.is_valid():
				business_form.save(commit=True)
				return index(request)

	return render(request,'dac/userProfile.html',context_dict)

@login_required
def user_reviews(request):
	context_dict = {'reviews':None}
	#get all the reviews from the current user
	user = UserProfile.objects.get(user=request.user)
	context_dict['reviews'] = Reviews.objects.filter(submitter=user)
	HttpResponse("needs a page")
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
