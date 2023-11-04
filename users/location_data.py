import os
import requests
from dotenv import load_dotenv

load_dotenv(verbose=True)

# LOCATION_API_KEY = os.getenv("LOCATION_API_KEY")

# url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={LOCATION_API_KEY}"
# data = {
#     "considerIp": True,
# }

# result = requests.post(url, data=data)

# print(result.text)

def get_location_data():
    LOCATION_API_KEY = os.getenv("LOCATION_API_KEY")
    if not LOCATION_API_KEY:
        raise ValueError("API_KEY가 없습니다.")

    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={LOCATION_API_KEY}"
    data = {
        "considerIp": True,
    }

    result = requests.post(url, data=data)
    
    if result.status_code == 200:
        return result.json()
        # return location_data["location"]["lat"], location_data["location"]["lng"]
    else:
        return None, None
    
# print(get_location_data())



# def get_location_by_ip(ip_adress, LOCATION_API_KEY):

#     url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={LOCATION_API_KEY}"
#     data = {
#         "considerIp": True,
#         "homeMobileCountryCode" : ip_adress
#     }

#     response = requests.post(url, json=data)
#     if response.status_code == 200:
#         location_data = response.json()
#         return location_data["location"]["lat"], location_data["location"]["lng"]
#     else:
#         return None, None

# print(get_location_by_ip("010", LOCATION_API_KEY))
