import requests
import json
import ids

url = "http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=47.2627&lon=11.3945&appid=%s" % ids.openweathermap_key
url2 = "http://api.openweathermap.org/data/2.5/forecast?q=Innsbruck&appid=%s" % ids.openweathermap_key

if __name__ == '__main__':
    response = requests.get(url).json()
    # print(json.dumps(response, indent=4, sort_keys=False))

    # example of searching
    filter = response["list"][10]["components"]["co"]
    print(filter)

    response = requests.get(url2).json()
    # print(json.dumps(response, indent=4, sort_keys=False))