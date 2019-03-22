from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.conf import settings
from os.path import join

class User(AbstractUser):
	is_business = models.BooleanField(default=False)

	def __str__(self):
		return self.username

class Ingredient(models.Model):
	MALTS = "MA"
	HOPS = "HO"
	OTHER = "OH"

	INGREDIENT_CATEGORIES = (
		(MALTS, "malts"),
		(HOPS, "hops"),
		(OTHER, "other")
	)

	name = models.CharField(max_length=30, unique=True)
	category = models.CharField(
		max_length=2,
		choices=INGREDIENT_CATEGORIES,
		default=OTHER
	)

	def __str__(self):
		return self.name

class Flavor(models.Model):
	BITTERNESS = "BI"
	SWEETNESS = "SW"
	COLOR = "CO"
	AROMA = "AR"
	TASTE = "TA"

	FLAVOR_CATEGORIES = (
		(BITTERNESS, "bitterness"),
		(SWEETNESS, "sweetness"),
		(COLOR, "color"),
		(AROMA, "aroma"),
		(TASTE, "taste")
	)

	name = models.CharField(max_length=30)
	category = models.CharField(
		max_length=2,
		choices=FLAVOR_CATEGORIES
	)

	def __str__(self):
		return self.name

class Beer(models.Model):
	name = models.CharField(max_length=30, unique=True)
	tagline = models.CharField(max_length=128)
	image = models.ImageField(upload_to='beer_images', blank=True)
	description = models.TextField(blank=False)
	abv = models.FloatField(blank=False)
	ibu = models.IntegerField(blank=False)
	og = models.IntegerField(blank=False)
	calories = models.IntegerField(blank=False)
	slug = models.SlugField(unique=True)

	ingredients = models.ManyToManyField(Ingredient)
	flavors = models.ManyToManyField(Flavor)
	
	def get_review_average(self):
		ratings = Review.objects.filter(beer=self)
		if ratings:
			return sum(rating.rating for rating in ratings)/len(ratings)
		return -1

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Beer, self).save(*args, **kwargs)

	def __str__(self):
		return self.name



class UserProfile(models.Model):
	user = models.OneToOneField(User)
	image = models.ImageField(upload_to='profile_images',default='profile_images/default.png')
	

	def __str__(self):
		return self.user.username

class Business(models.Model):
	name = models.CharField(max_length=256, unique=True)
	address = models.CharField(max_length=256)
	description = models.TextField()
	slug = models.SlugField(unique=True)
	owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE,
		primary_key=True
	)

	lng = models.FloatField(null=True)
	lat = models.FloatField(null=True)

	beers = models.ManyToManyField(Beer)
	image = models.ImageField(upload_to='business_images',default='business_images/default.png')

	class Meta:
		verbose_name_plural = 'Businesses'

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Business, self).save(*args, **kwargs)

	def __str__(self):
		return self.name + " (" + self.address + ")"

class Review(models.Model):
	rating = models.PositiveSmallIntegerField(default=1)
	review = models.TextField(blank=False)
	image = models.ImageField(upload_to='review_images')
	submitter = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	flavors = models.ManyToManyField(Flavor)
	beer = models.ForeignKey(Beer)

	def __str__(self):
		return self.submitter.user.username
