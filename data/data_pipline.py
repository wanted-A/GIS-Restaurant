import os
import django
import environ
import json
import math
import requests

"""
OpenAPI 활용
경기도_카페 데이터 수집 코드입니다.
"""

env = environ.Env()
env_file = os.path.join(os.path.dirname(__file__), ".env")
env.read_env(env_file)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

cafe_key = env("CAFE_ACCESSKEY")

url = f"https://openapi.gg.go.kr/Genrestrtcate?Key={cafe_key}&Type=json"
response = requests.get(url)


def request_data():
    """데이터 수집"""

    url = f"https://openapi.gg.go.kr/Genrestrtcate?Key={cafe_key}&Type=json"
    response = requests.get(url)

    list_total_count = response.json()["Genrestrtcate"][0]["head"][0][
        "list_total_count"
    ]
    total_page = math.ceil(list_total_count / 100)

    total_raw_data = []
    for page in range(1, total_page + 1):
        url = f"https://openapi.gg.go.kr/Genrestrtcate?Key={cafe_key}&Type=json&pIndex={page}"
        page_response = requests.get(url)
        raw_data = page_response.json()["Genrestrtcate"][1]["row"]
        total_raw_data += raw_data

    # 데이터 확인을 위해 json 파일로 저장
    with open(f"./data/total_place_data.json", "w", encoding="utf-8") as f:
        json.dump(total_raw_data, f, ensure_ascii=False, indent=4)


def data_processing():
    """데이터 전처리"""
    pass


def update_data():
    pass


def save_place_data(data):
    """데이터 DB에 저장"""
    pass


if __name__ == "__main__":
    request_data()
