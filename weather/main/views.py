from logging import exception
from urllib.error import HTTPError
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib
import config
from eprint import eprint
from geopy.distance import great_circle
def index(request):

    if request.method == 'POST':
        city = request.POST['city']
        print("User Lat: %s\t Lon: %s"%(request.POST['clientlatitude'],request.POST['clientlongitude']))       
         
        #find the Lattitude and Longitude of the searched location
        try:
            source = urllib.request.urlopen(
            'https://nominatim.openstreetmap.org/search?q=' 
                    + urllib.parse.quote(city) + '&format=json').read()
        except HTTPError as error:
            eprint.error("Received HTTPError from openstreetmap api call: %d" %(error.code))
            raise NotImplementedError
        list_of_data = json.loads(source)
        print("Searched Location Lat: %s\t Lon: %s"%(list_of_data[0]['lat'],list_of_data[0]['lon']))
           
        # Get weather information at the searched location, Using coordinates found by OSM
        try:
            source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?lat=' 
                    + urllib.parse.quote(list_of_data[0]['lat']) + '&lon=' + urllib.parse.quote(list_of_data[0]['lon']) + '&appid=' + config.apikey).read()
        except HTTPError as error:
            eprint.error("Received HTTPError from openweathermap api call: %d" %(error.code))
            if error.code == 404:
                #This is just placeholder code, this error conditions should not render the 404 page.
                return render(request, "main/404.html")
            else:
                return render(request, "main/index.html")
        
        # converting JSON data to a dictionary
        list_of_data = json.loads(source)
        print(great_circle((request.POST['clientlatitude'],request.POST['clientlongitude']), (list_of_data['coord']['lat'],list_of_data['coord']['lon'])).km)
        # data for variable list_of_data
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ' '
                        + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + 'k',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            "user_coordinate": request.POST['clientlongitude'] + ' '
                        + request.POST['clientlatitude'],
            "distance":str(great_circle((request.POST['clientlatitude'],request.POST['clientlongitude']), (list_of_data['coord']['lat'],list_of_data['coord']['lon'])).miles)
        }
        print(data)
    else:
        data ={}
    return render(request, "main/index.html", data)