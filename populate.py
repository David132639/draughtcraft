import os
import django
from django.core.files import File


def populate():

    print('Populating Database...')
    print('----------------------\n')

    username = 'admin'
    email = 'admin@admin.com'
    password = 'admin'

    create_super_user(username, email, password)

    flavors = {	"yellow": add_flavor('Yellow', Flavor.COLOR),
                "gold": add_flavor('Gold', Flavor.COLOR),
                "amber": add_flavor('Amber', Flavor.COLOR),
                "cedar": add_flavor('Cedar', Flavor.AROMA),
                "heather": add_flavor('Heather', Flavor.AROMA),
                "caramel": add_flavor('Caramel', Flavor.AROMA),
                "orange": add_flavor('Orange', Flavor.AROMA),
                "citrus": add_flavor('Citrus', Flavor.AROMA),
                "sweet": add_flavor('Sweet', Flavor.AROMA),
                "fresh": add_flavor('Fresh', Flavor.AROMA),
                "zesty": add_flavor('Zesty', Flavor.AROMA),

                "sharp": add_flavor('Sharp', Flavor.TASTE),
                "crisp": add_flavor('Crisp', Flavor.TASTE),
                "biscuity": add_flavor('Biscuity', Flavor.TASTE),
                "fruity": add_flavor('Fruity', Flavor.TASTE),
                "herbal": add_flavor('Herbal', Flavor.TASTE),
                "honey": add_flavor('Honey', Flavor.TASTE),
                "piney": add_flavor('Piney', Flavor.TASTE),
                "med_bitter": add_flavor('Medium Bitterness', Flavor.TASTE)
                }

    ingredients = {"wheat": add_ingredient("Malted Wheat", Ingredient.MALTS),
                   "oats": add_ingredient("Oats", Ingredient.MALTS),
                   "vmalt": add_ingredient("Vienna Malt", Ingredient.MALTS),
                   "prye": add_ingredient("Pale Rye", Ingredient.MALTS),
                   "pcrys": add_ingredient("Pale Crystal", Ingredient.MALTS),
                   "lmalt": add_ingredient("Lager Malt", Ingredient.MALTS),
                   "cascade": add_ingredient("Cascade", Ingredient.HOPS),
                   "fgold": add_ingredient("First Gold", Ingredient.HOPS),
                   "mosaic": add_ingredient("Mosaic", Ingredient.HOPS),
                   "citra": add_ingredient("Citra", Ingredient.HOPS)
                   }

    ceasar = add_beer(name='Caesar Augustus',
             img_name="caesar-augustus.jpeg",
             tagline='Lager / IPA hybrid',
             description="This Lager / IPA hybrid is a revolution in \
				refreshment and flavour. All the crisp clean notes of the \
				finest lager but with the discrete bitter finish of a \
				well-balanced IPA. It's not confused about what it wants to \
				be, it's just the best of both worlds.",
             abv=4.1,
             ibu=33,
             og=1041,
             calories=38,
             flavors=[flavors["fresh"], flavors["zesty"],
                      flavors["fruity"], flavors["sharp"], flavors["crisp"],
                      flavors["biscuity"]],
             ingredients=[ingredients["wheat"], ingredients["oats"], ingredients["prye"]])

    joker = add_beer(name='Joker IPA',
             img_name="joker-ipa.jpg",
             tagline='Wickedly Hoppy',
             description="There's at least one in every pack and this is \
				our very own agent of chaos. Created from a complex layer of \
				malts and blended hops, this well balanced IPA delivers \
				satisfaction every time. Golden in the glass, fruity on the \
				nose with hints of cedar. Joker IPA is Bitter/Sweet, full of \
				flavour and is sure to put a smile on your face.",
             abv=5.0,
             ibu=26,
             og=1051,
             calories=47,
             flavors=[flavors["yellow"], flavors["gold"],
                      flavors["cedar"], flavors["caramel"], flavors["orange"],
                      flavors["citrus"], flavors["biscuity"], flavors["fruity"],
                      flavors["herbal"], flavors["piney"], flavors["med_bitter"]],
             ingredients=[ingredients["wheat"], ingredients["fgold"], ingredients["prye"], ingredients["mosaic"]])

    fraoch =add_beer(name='Fraoch',
             img_name="default.jpg",
             tagline='Heather Ale',
             description='The Original Craft Beer; brewed in Scotland \
				since 2000 B.C. The Brotherhood have been guardians of the \
				ancient Gaelic recipe for "Leann Fraoch" (Heather Ale) since \
				1988 & are proud to be the only brewery still producing this \
				unique style of beer & distributing it world-wide. A light \
				amber ale with floral-peaty aroma, full malt character, and \
				a spicy herbal finish - This beer allows you to literally \
				pour 4000 years of Scottish history into a glass.',
             abv=5.0,
             ibu=12,
             og=1050,
             calories=48,
             flavors=[flavors["gold"], flavors["amber"],
                      flavors["fresh"],
                      flavors["citrus"]],
             ingredients=[ingredients["wheat"], ingredients["fgold"], ingredients["pcrys"], ingredients["mosaic"]])

    add_beer(name='Birds & Bees',
             img_name="default.jpg",
             tagline='Golden Summer Ale',
             description='Brewed for the summer evenings when we down \
				tools for the day and retire to the beer garden. This bright, \
				golden ale is a blend of lager malt, Cascade, Amarillo & \
				Nelson Sauvin hops with a late infusion of elderflower. \
				Fruity, aromatic and deliciously refreshing.',
             abv=4.3,
             ibu=25,
             og=1045,
             calories=41,
             flavors=[flavors["gold"],
                      flavors["zesty"], flavors["sweet"],
                      flavors["herbal"], flavors["honey"]],
             ingredients=[ingredients["wheat"], ingredients["fgold"], ingredients["pcrys"],
                          ingredients["mosaic"], ingredients["lmalt"], ingredients["cascade"]])

    #create some user and business accounts
    spam,spamProfile = create_user_account("spam_user","spam_user@bar.com","starwars")
    ham,hamProfile = create_user_account("ham_user","ham_user@bar.com","superSecurePassword")
    bus,busProfile = create_user_account("bus_user","bus_user@bar.com","piney",business=True)

    #setup of sample business
    create_business(user=busProfile,
                    name="DRAM!",
                    address="232 Woodlands Rd, Glasgow G3 6ND",
                    description="Lively destination for sporting events and parties",
                    stocks=[joker,ceasar]
                    )


    #creating user reviews
    create_beer_review(user_profile=hamProfile,beer=joker,content="Good beer",rating=5)
    create_beer_review(user_profile=spamProfile,beer=joker,content="ok beer",rating=2)
    create_beer_review(user_profile=spamProfile,beer=ceasar,content="meh beer",rating=1)

    print('\nSuperUser:', User.objects.get(is_superuser=True).username)
    print('\n' + ('=' * 80) + '\n')

    


def add_ingredient(name, category):
    i, created = Ingredient.objects.get_or_create(name=name, category=category)

    print('- Ingredient: {0}, Created: {1}'.format(str(i), str(created)))
    return i


def add_flavor(name, category):
    f, created = Flavor.objects.get_or_create(name=name, category=category)

    print('- Flavor: {0}, Created: {1}'.format(str(f), str(created)))
    return f


def add_beer(name, img_name, tagline, description, abv, ibu, og, calories, flavors, ingredients):

    img_file = os.path.join("beer_images", img_name)
    b, created = Beer.objects.get_or_create(name=name,
                                            image=img_file,
                                            tagline=tagline,
                                            description=description,
                                            abv=abv,
                                            ibu=ibu,
                                            og=og,
                                            calories=calories)
    b.flavors.add(*flavors)
    b.ingredients.add(*ingredients)
    print('- Beer: {0}, Created: {1}'.format(str(b), str(created)))
    return b


def create_super_user(username, email, password):
    try:
        u = User.objects.create_superuser(username, email, password)
        return u
    except IntegrityError:
        pass

def create_user_account(username,email,password,business=False):
    user,created = User.objects.get_or_create(username=username,email=email,password=password,is_business=business)
    print("- User: {0} Created: {1}".format(str(user),str(created)))
    user_profile,created = UserProfile.objects.get_or_create(user=user)
    print("\tUser profile: {0} Created: {1}".format(str(user_profile),str(created)))
    return user,user_profile

def create_business(user,name,address,description,stocks=[],):
    google_addr_info = get_place_info(address)

    business,created = Business.objects.get_or_create(owner=user,
                                            name=name,
                                            address=google_addr_info["address"],
                                            description=description,
                                            lat=google_addr_info["lat"],
                                            lng=google_addr_info["lng"],
                                            )
    for stock in stocks:
        business.beers.add(stock)
    print("- Business: {0} Created: {1}".format(str(business),str(created)))


def create_beer_review(user_profile,beer,content,rating):
    review,created = Review.objects.get_or_create(submitter=user_profile,
                                                beer=beer,
                                                rating=rating,
                                                review=content)
    print("- Review: {0} Created: {1}".format(str(review),str(created)))

if __name__ == '__main__':
    print('\n' + ('=' * 80) + '\n')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'wad_team_project.settings')
    django.setup()

    from dac.models import Ingredient, Flavor, Beer, Business, UserProfile
    from dac.models import User, Review
    from django.db import IntegrityError
    from dac.services import get_place_info

    populate()
