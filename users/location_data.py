import os
import requests
from dotenv import load_dotenv


# 환경 변수를 로드하는 부분
load_dotenv(verbose=True)

def get_location_data():
    LOCATION_API_KEY = os.getenv("LOCATION_API_KEY")
    if not LOCATION_API_KEY:
        raise Exception("API 키가 존재하지 않습니다.")

    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={LOCATION_API_KEY}"
    data = {"considerIp": True}
    result = requests.post(url, data=data)

    if result.status_code == 200:
        return result.json()
    else:
        return None, None

# print(get_location_data())
