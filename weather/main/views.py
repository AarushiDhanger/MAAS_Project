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
def index(request):

    if request.method == 'POST':
        city = request.POST['city']
        print(request.POST['clientlatitude'])
        print(request.POST['clientlongitude'])

        # source contain JSON data from API
        try:
            source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' 
                    + urllib.parse.quote(city) + '&appid=' + config.apikey).read()
        except HTTPError as error:
            eprint.error("Received HTTPError from openweathermap api call: %d" %(error.code))
            if error.code == 404:
                #This is just placeholder code, this error conditions should not render the 404 page.
                return render(request, "main/404.html")
            else:
                return render(request, "main/index.html")
        
        # converting JSON data to a dictionary
        list_of_data = json.loads(source)
  
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
        }
        print(data)
    else:
        data ={}
    return render(request, "main/index.html", data)