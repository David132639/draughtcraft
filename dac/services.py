import googlemaps
from django.conf import settings

GOOGLE_MAPS_FIELDS = ["geometry","name","formatted_address","place_id"]


def get_place_info(address):
    gmaps = googlemaps.Client(key=settings.GOOGLE_PLACES_API_KEY)

    place_results = gmaps.find_place(address,input_type="textquery",fields=GOOGLE_MAPS_FIELDS)

    print("place results: ",place_results)
    try:
        business = place_results["candidates"][0]
    except:
        return None
    lat = business["geometry"]["location"]["lat"]
    lng = business["geometry"]["location"]["lng"]
    name = business["name"]
    address = business["formatted_address"]
    return {"name" : name, "address" : address, "lat" : lat, "lng" : lng}
    