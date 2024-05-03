from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pgeocode
import pandas as pd

#function for the home page
def index(request):
    return render(request,'form.html')

#turn zipcode into latitude and longitude
def get_location(zip_code):
    nomi = pgeocode.Nominatim('us')
    location = nomi.query_postal_code(zip_code)

    #if the input is invalid, keep null value in the coordination set
    if pd.isna(location['latitude']) or pd.isna(location['longitude']):
        return (None, None)
    else:
        return (location['latitude'], location['longitude'])


def calculate(request):
    #get the zipcode input by the user
    zip1 = request.GET["zip1"]
    zip2 = request.GET["zip2"]

    #use get_location function to turn zipcode into coordinations
    loc1 = get_location(zip1)
    loc2 = get_location(zip2)

    if None in loc1 or None in loc2:
        error_message = "The zip code is unacceptable. Please enter a valid US zipcode. Only numbers are accepted. Do not enter any symbols like ,.$%^"
        return render(request, 'result.html', {"result": error_message})#if the zipcode is not recognized by the function (invalid), return error notification

    #keep 2 decimal places, use the geodesic function to return the distance in mile
    res = round(geodesic(loc1, loc2).miles, 2) 
    output = f'The Distance between {zip1} and {zip2} is {res} miles.' 
    return render(request,'result.html', {"result":output})