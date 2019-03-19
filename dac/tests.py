from django.test import TestCase
from django.core.urlresolvers import reverse

from dac.models import User
from dac.models import Ingredient, Flavor, Beer, Business, UserProfile, Review
from django.db import IntegrityError

import populate


class IndexTestCase(TestCase):
    def setUp(self):
        Beer.objects.get_or_create(
            name="testbeer", abv=5, ibu=5, og=5, calories=5)
        self.response = self.client.get(reverse('index'))

    def test_index_loads(self):
        self.assertIn('Draught and Craft'.lower(),
                      self.response.content.decode('ascii').lower())

    def test_index_has_components(self):
        self.assertIn('Top Beers'.lower(),
                      self.response.content.decode('ascii').lower())
        self.assertIn('Top Pubs'.lower(),
                      self.response.content.decode('ascii').lower())
        self.assertIn('testbeer'.lower(),
                      self.response.content.decode('ascii').lower())
    
    def test_index_login_signup_displayed_when_not_logged_in(self):
        self.assertIn('sign in'.lower(),
                      self.response.content.decode('ascii').lower())

        self.assertIn('register'.lower(),
                      self.response.content.decode('ascii').lower())

class BeerListTestCase(TestCase):
    def setUp(self):
        Beer.objects.get_or_create(
            name="testbeer", abv=5, ibu=5, og=5, calories=5)
        Beer.objects.get_or_create(
            name="otherbeer", abv=5, ibu=5, og=5, calories=5, description="a"*1000)

        self.response = self.client.get(reverse('beers'))

    def test_beer_list_loads(self):
        self.assertIn('All Available Beers'.lower(),
                      self.response.content.decode('ascii').lower())

    def test_beer_list_displays_all_beers(self):
        self.assertIn('testbeer'.lower(),
                      self.response.content.decode('ascii').lower())
        self.assertIn('otherbeer'.lower(),
                      self.response.content.decode('ascii').lower())

    def test_beer_description_has_read_more_link(self):
        self.assertIn('read more'.lower(),
                      self.response.content.decode('ascii').lower())


class BeerDetailsTestCase(TestCase):
    def setUp(self):
        self.f, _ = Flavor.objects.get_or_create(name="zesty", category=Flavor.AROMA)

        self.b, _ = Beer.objects.get_or_create(name="My Fancy Non-Offensive Beer", abv=5,
                                   ibu=5, og=5, calories=5, description="The quick brown fox")
        self.b.flavors.add(self.f)

        self.response = self.client.get(
            reverse('beers', args=['my-fancy-non-offensive-beer']))

    def test_beer_details_page_loads(self):
        self.assertIn('My Fancy Non-Offensive Beer'.lower(),
                      self.response.content.decode('ascii').lower())

    def test_beer_details_page_contains_description(self):
        self.assertIn('The quick brown fox'.lower(),
                      self.response.content.decode('ascii').lower())

    def test_beer_details_page_displays_no_review_info(self):
        self.assertIn('No reviews yet...'.lower(),
                      self.response.content.decode('ascii').lower())
    
    def test_beer_details_page_displays_tasting_notes(self):
        self.assertIn('zesty'.lower(),
                      self.response.content.decode('ascii').lower())
    
    def test_beer_details_page_displays_review_data_accurately(self):
        u = User.objects.create_superuser("admin", "admin@admin.admin", "admin")
        up = UserProfile.objects.create(user=u)

        r, _ = Review.objects.get_or_create(rating=2, review="pretty crap", submitter=up, beer=self.b)

        self.response = self.client.get(
            reverse('beers', args=['my-fancy-non-offensive-beer']))

        self.assertIn('2 out of 5'.lower(),
                      self.response.content.decode('ascii').lower())   

        self.assertIn('view reviews'.lower(),
                      self.response.content.decode('ascii').lower())

class LoginTestCase(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('auth_login'))
    
    def test_login_page_displayed(self):
        self.assertIn('login'.lower(),
                      self.response.content.decode('ascii').lower())
    
    def test_login_page_has_register_link(self):
        self.assertIn('register'.lower(),
                      self.response.content.decode('ascii').lower())
    
    def test_login_valid_username_password_detected(self):
        u = User.objects.create_superuser("admin", "admin@admin.admin", "pass")
        up = UserProfile.objects.create(user=u)

        self.response = self.client.post(reverse('auth_login'), {'username': 'admin', 'password': 'pass'})

        self.assertRedirects(self.response, reverse('index'))
        self.response = self.client.get(reverse('index'))

        self.assertIn('admin'.lower(),
                      self.response.content.decode('ascii').lower())

    def test_login_invalid_username_password_detected(self):
        self.assertNotIn('Please enter a correct username and password'.lower(),
                      self.response.content.decode('ascii').lower())

        self.response = self.client.post(reverse('auth_login'), {'username': 'wronguser', 'password': 'wrongpass'})

        self.assertIn('Please enter a correct username and password'.lower(),
                      self.response.content.decode('ascii').lower())
        