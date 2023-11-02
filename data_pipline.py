"""
OpenAPI 활용(데이터 수집, 전처리, 저장)
"""

import os
import json
import pandas as pd
import math
import requests
import django
import environ

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from restaurants.models import Restaurant

env = environ.Env()
env_file = os.path.join(os.path.dirname(__file__), ".env")
env.read_env(env_file)

API_AUTHENTICATE_KEY = env("API_AUTHENTICATE_KEY")

BUSINESS_TYPE = ["Genrestrtlunch","Genrestrtcate","Genrestrtmovmntcook"]

FIELDS = {
    "SIGUN_NM": "location_name",
    "SIGUN_CD": "location_code",
    "BIZPLC_NM": "restaurant_name",
    "LICENSG_DE": "license_date",
    "BSN_STATE_NM": "business_status_name",
    "CLSBIZ_DE": "closed_date",
    "LOCPLC_AR": "location_area",
    "GRAD_FACLT_DIV_NM": "water_supply_facility_name",
    "MALE_ENFLPSN_CNT": "male_worker_count",
    "YY": "year",
    "MULTI_USE_BIZESTBL_YN": "multi_use_yn",
    "GRAD_DIV_NM": "grade_division_name",
    "TOT_FACLT_SCALE": "total_facility_scale",
    "FEMALE_ENFLPSN_CNT": "female_worker_count",
    "BSNSITE_CIRCUMFR_DIV_NM": "business_site_around_name",
    "SANITTN_INDUTYPE_NM": "clean_industry_name",
    "SANITTN_BIZCOND_NM": "clean_business_type",
    "TOT_EMPLY_CNT": "total_worker_count",
    "REFINE_LOTNO_ADDR": "road_address",
    "REFINE_ROADNM_ADDR": "lot_num_address",
    "REFINE_ZIP_CD": "zip_code",
    "REFINE_WGS84_LOGT": "latitude",
    "REFINE_WGS84_LAT": "longitude"
}

def get_page_count(api_url, business_type):
    """ 총 페이지 개수 구하는 함수 """

    response = requests.get(api_url)

    list_total_count = response.json()[business_type][0]["head"][0]["list_total_count"]
    total_page = math.ceil(list_total_count/100) # 총 페이지 수(페이지당 100개씩 보여질 경우)

    return total_page

def request_data(business_type):
    """ 데이터 수집 """

    api_url = f'https://openapi.gg.go.kr/{business_type}?KEY={API_AUTHENTICATE_KEY}&Type=json'
    total_page = get_page_count(api_url, business_type)
    
    total_raw_data = []
    for page in range(1, total_page + 1):
        url = f'{api_url}&pIndex={page}'
        page_response = requests.get(url)
        raw_data = page_response.json()[business_type][1]["row"]
        total_raw_data += raw_data
    return total_raw_data

def data_processing(raw_data):
    """ 데이터 전처리 """
    # json data를 DataFrame 형태로 변경
    df = pd.DataFrame(raw_data)

    # null 값 처리
    for field in FIELDS:
        # float
        if field in ["LOCPLC_AR", "TOT_FACLT_SCALE"]:
            df[field] = df[field].astype(float)
            df[field] = df[field].fillna(0.0)
        # int
        elif field in ["MALE_ENFLPSN_CNT", "FEMALE_ENFLPSN_CNT", "TOT_EMPLY_CNT"]:
            df[field] = pd.to_numeric(df[field])
            df[field] = df[field].fillna(0)
        # YN
        elif field in ["MULTI_USE_BIZESTBL_YN"]:
            df[field] = df[field].fillna("N")
        # date
        elif field in ["LICENSG_DE", "CLSBIZ_DE"]:
            df[field] = pd.to_datetime(df[field])
            df[field] = df[field].dt.strftime('%Y-%m-%d')
            df[field] = df[field].fillna(" ")
        # string
        else:
            # 양 끝 공백 제거
            df[field] = df[field].str.strip()
            df[field] = df[field].fillna(" ")
    
    # 내부 필드명으로 변경
    df.rename(columns=FIELDS, inplace=True)

    # 유일키 생성
    df['restaurant_code'] = df["restaurant_name"] + df["road_address"]

    # dataframe to json 저장
    # df.to_json('./data/json_data.json',orient='records', force_ascii=False, indent=4)

    data = df.to_dict('records')

    return data

def save_place_data(data):
    """ 데이터 DB에 저장 """
    for row in data:  
        try:
            Restaurant(**row).save()
        except Exception as e:
            print(row)
            continue

def run():
    # for business_type in BUSINESS_TYPE:

    # test: 이동음식
    raw_data = request_data("Genrestrtmovmntcook")
    data = data_processing(raw_data)
    save_place_data(data)

if __name__ == "__main__":
    run()