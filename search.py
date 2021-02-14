import sys
from io import BytesIO
import requests
from PIL import Image
from get_map_coordinates import get_toponym_size

toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    print("Error!")
    print(f"{response.status_code} ({response.reason})")
    exit()
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coordinates = toponym["Point"]["pos"]
toponym_longitude, toponym_latitude = toponym_coordinates.split(" ")
map_params = {
    "ll": ",".join([toponym_longitude, toponym_latitude]),
    "spn": ",".join(map(str, get_toponym_size(toponym))),
    "l": "map"
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
