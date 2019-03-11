from django import forms
from registration.forms import RegistrationForm
from dac.models import User,UserProfile

class RegisterForm(RegistrationForm):
	'''custom register form for business functionality'''
	is_business = forms.BooleanField(label="Business User",initial=False,required=False)
	class Meta:
		fields = ('username','is_business','email','password1','password2')
		model = User
	pass

class UserProfileForm(forms.ModelForm):
	avatar = forms.ImageField(label='profile image',required=False)
	class Meta:
		model = UserProfile
		fields = ('avatar',)

class UserProfileBusinessForm(UserProfileForm):
	business_name = forms.CharField()
	street_address = forms.CharField()
	country = forms.CharField()
	business_contact = forms.CharField()

	class Meta:
		model = UserProfile
		fields = ('avatar',
			'business_name',
			'street_address',
			'country',
			'business_contact')

class BeerReview(forms.Form):
	pass



