from django import forms
from registration.forms import RegistrationForm
from dac.models import User,UserProfile,Business


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
	address = forms.CharField(help_text="Street_address")
	description = forms.CharField(help_text="Business Description")
	slug = forms.CharField(help_text=forms.HiddenInput(),required=False)
	#need auto complete field for beers

	class Meta:
		model=Business
		exclude = ('beers','owner','slug')


RATING_CHOICES = [("1","1: Very Poor"),("2","2"),("3","3"),("4","4"),("5","5: Excellent"),]

class BeerReview(forms.ModelForm):
	rating = forms.Select(choices=RATING_CHOICES)
	pass



