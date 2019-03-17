from django import forms
from registration.forms import RegistrationForm
from dac.models import User,UserProfile,Business,Review


class RegisterForm(RegistrationForm):
	'''custom register form for business functionality'''
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

class BusinessForm(forms.ModelForm):
	name = forms.CharField(help_text="Business Name")
	address = forms.CharField(help_text="Street address")
	description = forms.Textarea()
	slug = forms.CharField(widget=forms.HiddenInput(),required=False)
	#need auto complete field for beers

	class Meta:
		model=Business
		fields = ('name','address','description')




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


