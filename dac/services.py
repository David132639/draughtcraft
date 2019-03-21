import googlemaps
from django.conf import settings

GOOGLE_MAPS_FIELDS = ["geometry","name","formatted_address","place_id",]
PLACE_FIELDS = ["photo",]

def get_image_reference(place_id,client=None):
    '''returns a reference object to the first image returned from teh places api
    or none if some error is encountered'''
    if not client:
        client = googlemaps.Client(key=settings.GOOGLE_PLACES_SERVER_API_KEY)

    place_results = client.place(place_id,fields=PLACE_FIELDS)
    
    #pull first image attribution from the returned data
    try:
        return place_results["result"]["photos"][0]
    except:
        return None

def get_image_from_reference(reference,filename,client=None):
    print(reference," ",filename)

    if not client:
        client = googlemaps.Client(key=settings.GOOGLE_PLACES_SERVER_API_KEY)

    '''Small file size to try and prevent throttling by google'''
    with open(filename,"wb") as outfile:
        for chunk in client.places_photo(
            reference["photo_reference"],max_width=175,max_height=175):

            if chunk:
                print("writing chunk")
                outfile.write(chunk)
    


def get_place_info(address):
    '''Returns basic fields about a given business from the given address
    or none if no results are returned from the api'''
    gmaps = googlemaps.Client(key=settings.GOOGLE_PLACES_SERVER_API_KEY)

    place_results = gmaps.find_place(address,input_type="textquery",fields=GOOGLE_MAPS_FIELDS)

    try:
        business = place_results["candidates"][0]
    except:
        return None
    lat = business["geometry"]["location"]["lat"]
    lng = business["geometry"]["location"]["lng"]
    name = business["name"]
    address = business["formatted_address"]
    place_id = business["place_id"]
    return {"place id":place_id,"name" : name, "address" : address, "lat" : lat, "lng" : lng}


def get_image_from_address(address,filename):
    '''downloads the first result image from google and stores it at filename
    returns false if this function fails'''
    place_info = get_place_info(address)
    if place_info:
        print("TERMINAL: got place info")
        reference = get_image_reference(place_info["place id"])
    else:
        return False

    if reference:
        print("TERMINAL: got image reference")
        get_image_from_reference(reference,filename)
        return True
    else:
        return False