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
        time = request.POST['time']
        print(time)
         
        #find the Lattitude and Longitude of the searched location
        try:
            source = urllib.request.urlopen(
            'https://nominatim.openstreetmap.org/search?q=' 
                    + urllib.parse.quote(city) + '&format=json').read()
        except HTTPError as error:
            eprint.error("Received HTTPError from openstreetmap api call: %d" %(error.code))
            raise NotImplementedError
        map_data = json.loads(source)
        if len(map_data) == 0:
            #No Location was found for the search request; figure out a nice way to handle this.
            raise NotImplementedError
           
        # Get weather information at the searched location, Using coordinates found by OSM
        try:
            source = urllib.request.urlopen(
            'https://api.openweathermap.org/data/2.5/onecall?lat=' 
                    + urllib.parse.quote(map_data[0]['lat']) + '&lon=' + urllib.parse.quote(map_data[0]['lon']) + '&appid=' + config.apikey + '&units=imperial').read()
        except HTTPError as error:
            eprint.error("Received HTTPError from openweathermap api call: %d" %(error.code))
            if error.code == 404:
                #This is just placeholder code, this error conditions should not render the 404 page.
                return render(request, "main/404.html")
            else:
                return render(request, "main/index.html")
        
        # converting JSON data to a dictionary
        list_of_data = json.loads(source)
        data = {
            "location_title":str(map_data[0]['display_name']),
            "coordinate": str(list_of_data['lat']) + ', '
                        + str(list_of_data['lon']),
            "temp": str(list_of_data['current']['temp']) + 'F',
            "pressure": str(list_of_data['current']['pressure']),
            "humidity": str(list_of_data['current']['humidity']),
            "user_coordinate": request.POST['clientlatitude'] + ', '
                        + request.POST['clientlongitude'],
            "distance":str(round(great_circle((request.POST['clientlatitude'],request.POST['clientlongitude']), (list_of_data['lat'],list_of_data['lon'])).miles,2)) + ' mi',
            "time":str(time)
        }
    else:
        data ={}
    return render(request, "main/main.html", data)
