from django.shortcuts import render,redirect,get_list_or_404
from .forms import CityForm
from .models import City
import requests
from django.contrib import messages

def home(request):
    form = CityForm()
    weather_data = []

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=city_name).count()
            if existing_city_count == 0:
                api_key = 'your_api_key_here'  
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=b73cf5c568d5881c8df0e6c401498eb2&units=metric'


                try:
                    response = requests.get(url)
                    response.raise_for_status() 
                    data = response.json()  
                    print(data)  

                    if data['cod'] == 200:
                        form.save()
                        messages.success(request, f"{city_name} Added Successfully...!!!")
                    else:
                        messages.error(request, "City Does Not Exist")
                except requests.exceptions.HTTPError as http_err:
                    messages.error(request, f"HTTP error occurred: {http_err}")
                except requests.exceptions.RequestException as err:
                    messages.error(request, f"Error occurred: {err}")
                except ValueError:
                    messages.error(request, "Invalid response received from the weather service.")
            else:
                messages.warning(request, "City already exists in the database.")

    form = CityForm()
    cities = City.objects.all()
    api_key = 'your_api_key_here'  

    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid=b73cf5c568d5881c8df0e6c401498eb2&units=metric'
        response = requests.get(url).json()
        if response['cod'] == 200:
            city_weather = {
                'city': city.name,
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'country': response['sys']['country'],
                'icon': response['weather'][0]['icon'],
            }
            weather_data.append(city_weather)
        else:
            messages.error(request, f"Could not retrieve data for {city.name}")

    context = {'data': weather_data, 'form': form}
    return render(request, "weatherapp.html", context)
 #ithu verapgm{'cities':cities,'form': form})

def delete_city(request,CName):
    cities = get_list_or_404(City, name=CName)
    
    # Delete each city object
    for city in cities:
        city.delete()
    
    # Redirect to the index page after deletion
    return redirect('Home')




               