from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from dac.models import Beer, Business,UserProfile,Review, Flavor
from dac.forms import UserProfileForm, BusinessForm, BeerReview
from registration.backends.simple.views import RegistrationView
from dac.services import get_place_info
import json


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

	#none specific so just a load of beers and send to the user
	if not beer_slug:
		context_dict['beers'] = Beer.objects.all()
		return render(request,'dac/beer_list.html',context_dict)

	#an explicit beer slug has been passed so just get that beer specifically
	beer = get_object_or_404(Beer,slug=beer_slug)
	ratings = Review.objects.filter(beer=beer)
	if ratings:
		context_dict["avg"] = sum(rating.rating for rating in ratings)/len(ratings)
	context_dict["beer"] = beer

	return render(request,'dac/beer.html',context_dict)

@login_required
def add_beer_review(request,beer_slug):
	#basic form for user adding review to a specific beer
	beer = get_object_or_404(Beer,slug=beer_slug)
	profile = UserProfile.objects.get(user=request.user)
	edit = False
	try:
	#check if the user has already submitted a review
	#pre populate form with previously submitted data
		prev_review = Review.objects.get(submitter=profile,beer=beer)
		flavours = ", ".join([str(x)for x in prev_review.flavors.all()])
		print("flavours already in teh form",flavours)

		form = BeerReview({'review':prev_review.review,"rating":prev_review.rating,'flavours':flavours})
		edit = True
	except Review.DoesNotExist:
	 	form = BeerReview()
	context_dict = {'beer':beer,'form':form}

	if request.method == "POST":
		if edit:
			form = BeerReview(request.POST,instance = prev_review)
		else:
			form = BeerReview(request.POST)
		if form.is_valid():
			#set these fields in teh model, a little cleaner than doing this
			#in teh view			
			review = form.save(commit=True,beer=beer,profile=profile)
			#must save before and after to satisfy many to many thing
			#must modify cleaned data
			review.flavors.clear()
			for flavor in form.cleaned_data['flavours']:
				try:
					review.flavors.add(Flavor.objects.get(name=flavor))
				except Flavor.DoesNotExist:
					pass
			review.save()
			return index(request)
	return render(request,'dac/add_review.html',context_dict)


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
	pub = Business.objects.get(slug=pub_slug)
	context_dict["pub"] = pub


	return render(request,'dac/pub.html',context_dict)

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
	context_dict = {"forms":[profile_form],'profile':profile}
	
	if request.user.is_business:
		#if the user is just registering
		if not hasattr(profile,'business'):
			business = Business.objects.create(owner=profile)
		else:
			business = profile.business
		stocks = ",".join([str(x)for x in business.beers.all()])
		business_form = BusinessForm({'name':business.name,'address':business.address,'description':business.description,
			"stocks":stocks})
		context_dict['forms'].append(business_form)
	
	if request.method == 'POST':
		profile_form = UserProfileForm(request.POST, request.FILES,instance=profile)
		form_list = [profile_form]

		#add the business form to the forms to be validated
		if request.user.is_business:
			business_form = BusinessForm(request.POST, request.FILES,instance=business)
			google_addr = get_place_info(business_form.data["address"])
			business.lat = google_addr["lat"]
			business.lng =google_addr["lng"]
			form_list.append(business_form)
		
		#check if all of teh forms are valid and then save
		if all([x.is_valid() for x in form_list]):
			for form in form_list:
				form.save(commit=True)
			return index(request)


	return render(request,'dac/userProfile.html',context_dict)


def map_api(request,pub_slug):
	if request.method != 'GET':
		return  HttpResponse(status=405)

	response = {}
	mime = 'application/json'
	pub = Business.objects.get(slug=pub_slug)
	response["lng"] = pub.lng
	response["lat"] = pub.lat

	return HttpResponse(json.dumps(response),mime)



def model_api(request,model_type):
	#only allow queries in these models
	allowed_models = {"beers":Beer,"flavours":Flavor}

	#get query and get results
	if request.is_ajax() and (model_type in allowed_models):
		entity = allowed_models[model_type]
		query = request.GET.get('term','')
		query_set = entity.objects.filter(name__contains=query)[:10]
		results = []
		#store as json like object
		for i,result in enumerate(query_set):
			result_entry = {}
			result_entry["id"] = i
			result_entry["label"] = result.name
			result_entry["value"]= result.name
			results.append(result_entry)
		data = json.dumps(results)
	else:
		data = 'fail'
	mime = 'application/json'
	return HttpResponse(data,mime)


@login_required
def user_reviews(request):
	context_dict = {'reviews':None}
	#get all the reviews from the current user
	user = UserProfile.objects.get(user=request.user)
	context_dict['reviews'] = Reviews.objects.filter(submitter=user)
	HttpResponse("needs a page")
	pass

def restricted(request):
	HttpResponse("Access Restricted")
	pass
