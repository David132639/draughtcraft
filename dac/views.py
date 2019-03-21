from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from dac.models import Beer, Business,UserProfile,Review, Flavor
from dac.forms import UserProfileForm, BusinessForm, BeerReview
from registration.backends.simple.views import RegistrationView
from dac.services import get_place_info, get_image_from_address
import json


# General site pages
def index(request):
	context_dict = {"beers":None,"business":None}

	#get top three rated beers but not implemented yet
	beers = sorted(Beer.objects.all(),key=lambda x: x.get_review_average(),reverse=True)[:3]
	print(beers)
	business = Business.objects.all()[:3]
	context_dict["business"] = business
	context_dict["beers"] = beers

	return render(request, 'dac/index.html', context=context_dict)

def sitemap(request):
	return render(request,'dac/sitemap.html')


#beer stuff
def beers(request,beer_slug=None):
	context_dict = {'beer': None,}

	#none specific so just a load of beers and send to the user
	if not beer_slug:
		context_dict['beers'] = Beer.objects.all()
		return render(request,'dac/beer_list.html',context_dict)

	#an explicit beer slug has been passed so just get that beer specifically
	beer = get_object_or_404(Beer,slug=beer_slug)
	avg = beer.get_review_average()
	if avg != -1:
		context_dict["avg"] = avg
	context_dict["stockists"] = Business.objects.filter(beers__in=[beer])
	print(context_dict["stockists"])
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
			form = BeerReview(request.POST,request.FILES,instance = prev_review)
		else:
			form = BeerReview(request.POST,request.FILES)
		if form.is_valid():			
			review = form.save(commit=True,beer=beer,profile=profile)
			#must save before and after to satisfy many to many relationship
			review.image = form.cleaned_data["image"]
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
	beer = get_object_or_404(Beer,slug=beer_slug)
	context = beer.name
	reviews = Review.objects.filter(beer=beer)

	context_dict["context"] = context
	context_dict["reviews"] = reviews

	return render(request,'dac/review_list.html',context_dict)


#pub stuff

def pubs(request,pub_slug=None):
	context_dict = {}

	if not pub_slug:
		context_dict['business'] = Business.objects.all()
		return render(request,'dac/pub_list.html',context_dict)
	pub = Business.objects.get(slug=pub_slug)
	context_dict["pub"] = pub


	return render(request,'dac/pub.html',context_dict)

def pubs_beers(request,pub_slug):
	pub = Business.objects.get(slug=pub_slug)
	context_dict["pub"] = pub
	return render(request,'dac/pub_stocks.html',context_dict)


def about(request):
	return render(request,'dac/about.html')


def privacy(request):
	return render(request,'dac/privacy.html')

#searching stuff
def search(request, query_string):
	beers = Beer.objects.filter(name__icontains=query_string) | Beer.objects.filter(description__icontains=query_string)
	businesses = Business.objects.filter(name__icontains=query_string)
	
	context_dict = {"business" : businesses, "beers": beers, "query": query_string}
	return render(request, 'dac/search_results.html', context_dict)

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
	profile_form = UserProfileForm({'image':profile.image})
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
			get_image_from_address(google_addr["address"],"{0}/business_images/{1}.jpg".format(settings.MEDIA_ROOT,business.slug))
			business.image = "business_images/{0}.jpg".format(business.slug)


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
	try:
		pub = Business.objects.get(slug=pub_slug)
	except Business.DoesNotExist:
		return HttpResponse(status=404)
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
	context_dict["context"] = request.user.username
	context_dict['reviews'] = Review.objects.filter(submitter=user)
	return render(request,'dac/review_list.html',context_dict)
	pass

def restricted(request):
	HttpResponse("Access Restricted")
	pass
