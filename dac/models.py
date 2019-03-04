from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

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

class Beer(models.Model):
	name = models.CharField(max_length=30, unique=True)
	tagline = models.CharField(max_length=128)
	image = models.ImageField(upload_to='beer_images', blank=True)

	description = models.TextField(blank=False)
	abv = models.FloatField(blank=False)
	ibu = models.IntegerField(blank=False)
	og = models.IntegerField(blank=False)
	calories = models.IntegerField(blank=False)

	ingredients = models.ManyToManyField(Ingredient)
	flavors = models.ManyToManyField(Flavor)

class Business(models.Model):
	name = models.CharField(max_length=256, unique=True)
	address = models.CharField(max_length=256)
	description = models.TextField()
	slug = models.SlugField(unique=True)

	beers = models.ManyToManyField(Beer)

	class Meta:
		verbose_name_plural = 'Businesses'

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.name + " (" + self.address + ")"

class Review(models.Model):
	rating = models.PositiveSmallIntegerField(default=1)
	review = models.TextField(blank=False)

	submitter = models.ForeignKey(User, on_delete=models.CASCADE)
	flavors = models.ManyToManyField(Flavor)
	beer = models.OneToOneField(Beer)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	avatar = models.ImageField(upload_to='profile_images', blank=True)
	is_business = models.BooleanField(default=False)

	business = models.OneToOneField(Business, on_delete=models.CASCADE,
		primary_key=True
	)

	def __str__(self):
		return self.user.username