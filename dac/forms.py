from django import forms
from registration.forms import RegistrationForm
from dac.models import User,UserProfile,Business,Review,Beer,Flavor


class RegisterForm(RegistrationForm):
	'''custom register form for businesses functionality'''
	is_business = forms.BooleanField(label="Business User",initial=False,required=False)
	class Meta:
		fields = ('username','is_business','email','password1','password2')
		model = User
	pass

class UserProfileForm(forms.ModelForm):
	image = forms.ImageField(help_text='Profile image:',required=False,)
	class Meta:
		model = UserProfile
		fields = ('image',)
	#overrride only allow images
	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)
		self.fields['image'].widget.attrs.update({'type':'image','accept':'image/*'})




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

	def clean(self):
		cleaned_data = super(BusinessForm,self).clean()

		if "stocks" in cleaned_data:
			cleaned_data["stocks"] = [x.strip() for x in cleaned_data["stocks"].split(",")]

		return cleaned_data


	def save(self,commit=True):
		business = super(BusinessForm,self).save(commit=False)
		business.beers.clear()
		for beer in self.cleaned_data['stocks']:
			try:
				business.beers.add(Beer.objects.get(name=beer))
			except Beer.DoesNotExist:
				pass
		if commit:
			business.save()
		return business


RATING_CHOICES = [(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5"),]

class BeerReview(forms.ModelForm):
	image = forms.ImageField(help_text='Image of your beer',required=False,)
	rating = forms.ChoiceField(help_text="Rating",choices=RATING_CHOICES)
	flavours = forms.CharField(help_text="Flavour profile",required=False)
	review = forms.CharField(widget=forms.Textarea(),help_text="Review text")


	class Meta:
		model = Review
		fields = ("rating",'flavours',"review")

	#override to set context for autocomplete input and for star rating bar
	def __init__(self, *args, **kwargs):
		super(BeerReview, self).__init__(*args, **kwargs)
		self.fields['rating'].widget.attrs.update({'id':'bar_rating'})
		self.fields['flavours'].widget.attrs.update({'id':'form_auto','autocomplete':'on','data-context':'flavours'})
		self.fields['image'].widget.attrs.update({'type':'image','accept':'image/*'})

	def clean(self):
		cleaned_data = super(BeerReview,self).clean()
		if "flavours" in cleaned_data:
			cleaned_data["flavours"] = [x.strip() for x in cleaned_data['flavours'].split(",")]

		if "ratings" in cleaned_data and (cleaned_data["ratings"]> 0 or cleaned_data["ratings"] < 0):
			raise ValidationError("rating outwith accepted ie. 0-5 inclusive")

		return cleaned_data

	def save(self,commit=True,*args,**kwargs):
		instance = super(BeerReview,self).save(commit=False)
		if "profile" in kwargs:
			instance.submitter = kwargs["profile"]
		if "beer" in kwargs:
			instance.beer = kwargs["beer"]

		if commit:
			instance.save()
		return instance
