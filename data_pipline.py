import requests
import re
import json
import os
import django
import environ
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

env = environ.Env()
env_file = os.path.join(os.path.dirname(__file__), ".env")
env.read_env(env_file)

from restaurants.models import Restaurant

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
    "REFINE_WGS84_LAT": "longitude",
}


# OPEN API 사용시 참고사항
# 1. response 자체는 리스트
# 2. response[0]은 'head'라는 키 값을 갖는 딕셔너리
# 3. 예) {'head': [{'list_total_count': 16}, {'RESULT': {'CODE': 'INFO-000', 'MESSAGE': '정상 처리되었습니다.'}}, {'api_version': '1.0'}]}
# 4. response[1]은 'row'라는 키 값을 갖는 딕셔너리
# 5. 예) {'row': [{'SIGUN_NM': '평택시', 'SIGUN_CD': '41220', 'BIZPLC_NM': '(주)비앤비', 'LICENSG_DE': '20120823', 'BSN_STATE_NM': '폐업', 'CLSBIZ_DE': '20130401', 'LOCPLC_AR': None, 'GRAD_FACLT_DIV_NM': '상수도전용', 'MALE_ENFLPSN_CNT': None, 'YY': None, 'MULTI_USE_BIZESTBL_YN': 'N', 'GRAD_DIV_NM': None, 'TOT_FACLT_SCALE': None, 'FEMALE_ENFLPSN_CNT': None, 'BSNSITE_CIRCUMFR_DIV_NM': '기타', 'SANITTN_INDUTYPE_NM': None, 'SANITTN_BIZCOND_NM': '이동조리', 'TOT_EMPLY_CNT': None, 'REFINE_LOTNO_ADDR': '경기도 평택시 오성면 죽리 19번지', 'REFINE_ROADNM_ADDR': '경기도 평택시 오성면 서동대로 2064-1', 'REFINE_ZIP_CD': '17926', 'REFINE_WGS84_LOGT': '126.9725130', 'REFINE_WGS84_LAT': '37.0065480'}


BUSINESS_TYPE = [
    "Genrestrtmovmntcook",  # 이동조리
    "Genrestrtcate",  # 까페
    "Genrestrtlunch",  # 김밥/도시락
]


# 총 데이터 갯수를 수집하여 반환하는 함수
def get_count(business_type):
    url = f"https://openapi.gg.go.kr/{business_type}"

    parameters = {
        "KEY": env("OPEN_API_KEY"),
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
    }

    try:
        response = (
            json.loads(requests.get(url, params=parameters).text)[business_type][0]
            .get("head")[0]
            .get("list_total_count")
        )
        return response
    except Exception as e:
        print(f"get_count error : {e}")


# 실제 미가공 데이터를 수집하여 반환하는 함수
def get_row(params, business_type):
    url = f"https://openapi.gg.go.kr/{business_type}"

    try:
        response = json.loads(requests.get(url, params=params).text)[business_type][
            1
        ].get("row")
        return response
    except Exception as e:
        print(f"get_row error : {e}")


# 데이터 전처리하는 함수
def preprocess_data(raw_data):
    # null 값 처리
    for field in FIELDS:
        try:
            if field in [
                "LOCPLC_AR",
                "TOT_FACLT_SCALE",
                "MALE_ENFLPSN_CNT",
                "FEMALE_ENFLPSN_CNT",
                "TOT_EMPLY_CNT",
            ]:
                raw_data[field] = raw_data[field] if raw_data[field] else 0

            elif field in ["REFINE_WGS84_LOGT", "REFINE_WGS84_LAT"]:
                raw_data[field] = float(raw_data[field]) if raw_data[field] else 00.0000

            elif field in ["MULTI_USE_BIZESTBL_YN"]:
                raw_data[field] = raw_data[field] if raw_data[field] else "N"

            elif field in ["LICENSG_DE", "CLSBIZ_DE"]:
                raw_data[field] = raw_data[field] if raw_data[field] else "0000-00-00"
                raw_data[field] = (
                    raw_data[field]
                    if bool(re.match(r"\d{4}-\d{2}-\d{2}", raw_data[field]))
                    else f"{raw_data[field][:4]}-{raw_data[field][4:6]}-{raw_data[field][6:8]}"
                )

            else:
                raw_data[field] = raw_data[field].strip() if raw_data[field] else ""

        except Exception as e:
            print(f"preprocess_data error : {field}, {e}")
            continue

    return raw_data


# 전처리된 데이터를 실제 저장하는 함수
def save_raw_data(total_list, page):
    for raw_data in total_list:
        try:
            preprocessed_data = preprocess_data(raw_data)
            restaurant_code = f'{preprocessed_data.get("BIZPLC_NM")}|{preprocessed_data.get("REFINE_LOTNO_ADDR")}|{preprocessed_data.get("LICENSG_DE")}'

            # 근데 여기서 continue하면 업데이트가 안됨....
            if Restaurant.objects.filter(restaurant_code=restaurant_code).exists():
                continue

            mapped_data = {FIELDS[k]: v for k, v in preprocessed_data.items()}
            mapped_data["restaurant_code"] = restaurant_code

            Restaurant(**mapped_data).save()

        except Exception as e:
            response = {
                "error_message": e,
                "error_page": page,
                "error_point": raw_data.get("BIZPLC_NM"),
            }
            print(f"save_raw_data error : {response}")
            continue


# 페이지별로 데이터 저장을 요청하는 함수
# celery 미적용시: 0:03:29.111738
def raw_data_handler():
    for business_type in BUSINESS_TYPE:
        list_total_count = get_count(business_type)

        for i in range((list_total_count // 100) + 1):
            total_list = get_row(
                {
                    "KEY": env("OPEN_API_KEY"),
                    "Type": "json",
                    "pIndex": i + 1,
                    "pSize": 100,
                },
                business_type,
            )
            save_raw_data(total_list, i + 1)


if __name__ == "__main__":
    Restaurant.objects.all().delete()

    start = time.time()

    raw_data_handler()

    print("실행시간 : ", time.time() - start)
