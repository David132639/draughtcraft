from django import forms
from registration.forms import RegistrationForm
from dac.models import User,UserProfile,Business,Review,Beer,Flavor


class RegisterForm(RegistrationForm):
	'''custom register form for businesses'''
	is_business = forms.BooleanField(label="Business User",initial=False,required=False)
	class Meta:
		fields = ('username','is_business','email','password1','password2')
		model = User
	pass

class UserProfileForm(forms.ModelForm):
	avatar = forms.ImageField(help_text='profile image',required=False,)
	class Meta:
		model = UserProfile
		fields = ('avatar',)
	#overrride only allow images
	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)
		self.fields['avatar'].widget.attrs.update({'type':'image','accept':'image/*'})

class BusinessForm(forms.ModelForm):
	name = forms.CharField(help_text="Business Name")
	address = forms.CharField(help_text="Street address")
	description = forms.CharField(required=False, help_text="Business Description", widget=forms.Textarea())
	stocks = forms.CharField(help_text='Tell us what beers your business stocks')
	slug = forms.CharField(widget=forms.HiddenInput(),required=False)
	#need auto complete field for beers
	class Meta:
		model=Business
		fields = ('name','address','description','stocks')

	#override to set context for autocomplete input
	def __init__(self, *args, **kwargs):
		super(BusinessForm, self).__init__(*args, **kwargs)
		self.fields['stocks'].widget.attrs.update({'id':'form_auto','autocomplete':'on','data-context':"beers"})

	def save(self,commit=True):
		business = super(BusinessForm,self).save(commit=False)
		for beer in self.cleaned_data['stocks'].strip().split(','):
			try:
				print(beer)
				business.beers.add(Beer.objects.get(name=beer))
				print("added beer called: ",beer)
			except Beer.DoesNotExist:
				pass
		if commit:
			business.save()
		return business


RATING_CHOICES = [(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5"),]

class BeerReview(forms.ModelForm):
	rating = forms.ChoiceField(help_text="rating",choices=RATING_CHOICES)
	flavours = forms.CharField(help_text="flavour profile")
	reivew = forms.Textarea()

	class Meta:
		model = Review
		fields = ("rating","review")

	#override to set context for autocomplete input and for star rating bar
	def __init__(self, *args, **kwargs):
		super(BeerReview, self).__init__(*args, **kwargs)
		self.fields['rating'].widget.attrs.update({'id':'bar_rating'})
		self.fields['flavours'].widget.attrs.update({'id':'form_auto','autocomplete':'on','data-context':'flavours'})
	
	def save(self,commit=True):
		review = super(BeerReview,self).save(commit=False)
		for flavor in self.cleaned_data['flavours'].strip().split(','):
			try:
				review.flavors.add(Flavor.objects.get(name=flavor))
			except Flavor.DoesNotExist:
				pass
		if commit:
			review.save()
		return review
