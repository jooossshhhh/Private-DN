import openmeteo_requests
import requests,os,datetime
import requests_cache
import pandas as pd
from retry_requests import retry
from dotenv import load_dotenv


load_dotenv()
WEATHER_API = os.getenv('WEATHER_API_KEY')
def bestWeather(zipcode):
    #zipcode = "37122"
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    #Set up API openweathermap to get lat & long
    base_url = "https://api.openweathermap.org"
    weather_api = WEATHER_API

    geoip = base_url+"/geo/1.0/zip?zip="+zipcode+"&appid="+weather_api
    georesponse = requests.get(geoip)
    x=georesponse.json()
    lat = x['lat']
    lng = x['lon']
    weather_url = base_url + "/data/2.5/weather?lat="+str(lat)+"&lon="+str(lng)+"&appid="+weather_api+"&units=imperial"
    response = requests.get(weather_url)
    y=response.json()
    #pprint(y)
    icon_image = "https://openweathermap.org/img/wn/" + y['weather'][0]['icon'] + "@2x.png"
    degree_sign = u'\N{DEGREE SIGN}'
    sunrise = datetime.datetime.fromtimestamp(y['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.datetime.fromtimestamp(y['sys']['sunset']).strftime('%H:%M')
    city = str(y['name'])
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "daily": ["temperature_2m_max", "temperature_2m_min", "uv_index_max", "precipitation_sum"],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "America/Chicago",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")


    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_uv_index_max = daily.Variables(2).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(3).ValuesAsNumpy()

    highlow = 'High : ' + str(int(daily_temperature_2m_max))+degree_sign + '<br>Low : ' +str(int(daily_temperature_2m_min))+degree_sign
    sun = 'Sunrise : ' + str(sunrise) + '<br>Sunset : ' + str(sunset)
    uv_max = 'Max UV Index : ' + str(int(daily_uv_index_max))

    weather_template = '<hr><h3>Weather for ' + city + '</h3><br><p ><table><tr><th>' + highlow  + '<br>' + sun + '<br>' + uv_max + "</th><th style='padding-left:0.8em'><img src='" + icon_image +"'/></th></tr></table></p>"
    # weather_template = '<hr><h3>Weather for ' + city + '</h3><br><p >' + highlow  + '<br>' + sun + '<br>' + humidity + "</p>"
    return weather_template


if __name__ == "__main__":
    from pprint import pprint
    weather = bestWeather('37122')
    pprint(weather)