from django import forms
from registration.forms import RegistrationForm
from dac.models import User

class RegisterForm(RegistrationForm):
	'''custom register form for business functionality'''
	is_business = forms.BooleanField(label="Business User",initial=False,required=False)
	class Meta:
		fields = ('username','is_business','email','password1','password2')
		model = User
	pass