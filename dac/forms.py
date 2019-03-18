from django import forms
from registration.forms import RegistrationForm
from dac.models import User,UserProfile,Business,Review,Beer
from dal import autocomplete


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

	def __init__(self, *args, **kwargs):
		super(BusinessForm, self).__init__(*args, **kwargs)
		self.fields['stocks'].widget.attrs.update({'id':'beer_auto','autocomplete':'on'})

RATING_CHOICES = [(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5"),]

class BeerReview(forms.ModelForm):
	rating = forms.ChoiceField(help_text="rating",choices=RATING_CHOICES)
	reivew = forms.Textarea()

	class Meta:
		model = Review
		fields = ("rating","review")

	#force the select field to have a bar rating id
	def __init__(self, *args, **kwargs):
		super(BeerReview, self).__init__(*args, **kwargs)
		self.fields['rating'].widget.attrs.update({'id':'bar_rating'})


