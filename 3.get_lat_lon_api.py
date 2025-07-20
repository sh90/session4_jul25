# Let's understand how API calling works in Python
#pip install requests
import requests

def get_lat_long_api():
    GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
    city_name = "tokyo"
    params = {
        'name': city_name,
        'count': 1
    }
    response = requests.get(GEOCODING_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            lat = data['results'][0]['latitude']
            lon = data['results'][0]['longitude']
            print( lat, lon)
        else:
            print( None, None)
    else:
        print( None, None)
    return lat, lon
def get_weather_api(lat,lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['current_weather']
        print(f"The temperature is {weather['temperature']}°C with a wind speed of {weather['windspeed']} km/h.")
    else:
        print("Sorry, couldn't retrieve the weather.")

if __name__ == "__main__":
    lat,lon = get_lat_long_api()
    get_weather_api(lat,lon)
