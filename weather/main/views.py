import datetime
import time;
from logging import exception
from math import floor
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
    #try:
    if request.method == 'POST':
        city = request.POST['city']
        #Convert time the user gave into the UTC time zone that the weather api uses.
        usertime = request.POST['time']
        offset = request.POST['clienttimeoffset']
        splittime = usertime.split(':');
        utctime = str((int(splittime[0]) + floor(int(offset)/60))%24) + ":" + str((int(splittime[1])+int(offset))%60)
        current_time = datetime.datetime.now() 
        unixtime = int(time.mktime(datetime.datetime(current_time.year, current_time.month, current_time.day, int(splittime[0]) if int(splittime[1]) < 30 else int(splittime[0]) + 1, 0).timetuple()))
        
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
        
        settemp = None;
        icon = None;
        for n in list_of_data["hourly"]:
            if n["dt"] == unixtime:
                settemp = n["temp"]
                icon = str(n['weather']).split('\'')[13]
                eprint.info("timematch found with temp: ",settemp)
                break
        if settemp == None:
            eprint.error("Failed to find the temperature for the time given, reverting to current time")
            settemp = list_of_data['current']['temp']
            icon = str(list_of_data['current']['weather']).split('\'')[13]
        
        weathercomment = None;
        if settemp > 100:
            weathercomment = "Make sure that your AC is working!"
        elif settemp > 80 :
            if int(splittime[0]) > 7 and int(splittime[0]) < 18:
                weathercomment = "You might want to wear sunscreen, It's hot outside!"
            else:
                weathercomment = "You might not get sunburn, but you'll still feel its heat!"
        elif settemp > 70:
            weathercomment = "Its a nice day outside, be sure to enjoy it!"
        elif settemp > 60:
            weathercomment = "The weather is average, a good day to get work done!"
        elif settemp > 45:
            weathercomment = "The weather is a bit chilly, be sure to bring a jacket!"
        else:
            weathercomment = "It's very cold! Watch out"

        data = {
            "location_title":str(map_data[0]['display_name']).split(',')[0],
            "coordinate": str(list_of_data['lat']) + ', '
                        + str(list_of_data['lon']),
            "temp": str(settemp) + 'F',
            "pressure": str(list_of_data['current']['pressure']),
            "humidity": str(list_of_data['current']['humidity']),
            "user_coordinate": request.POST['clientlatitude'] + ', '
                        + request.POST['clientlongitude'],
            "distance":str(round(great_circle((request.POST['clientlatitude'],request.POST['clientlongitude']), (list_of_data['lat'],list_of_data['lon'])).miles,2)),
            "comment":weathercomment,
            "imageid":icon,
        }
    else:
        data ={}
    return render(request, "main/main.html", data)
    #except:
    #    return render(request, "main/404.html")

