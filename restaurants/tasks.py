from __future__ import absolute_import, unicode_literals

from celery import shared_task

from rest_framework import status

from config.settings import env
from config.celery import app
from .models import RawData
from .serializers import RawDataSerializer

import requests
import json
import re


business_type_list = [
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
    except Exception as ex:
        return ex


# 실제 미가공 데이터를 수집하여 반환하는 함수
def get_row(params, business_type):
    url = f"https://openapi.gg.go.kr/{business_type}"

    try:
        response = json.loads(requests.get(url, params=params).text)[business_type][
            1
        ].get("row")
        return response
    except Exception as ex:
        return ex


# 데이터 전처리하는 함수
def preprocess_data(raw_data):
    # 미가공 데이터(dict)를 받아 None 여부 확인하고 기본값 설정하는 함수
    def get_value_or_default(key, default_value):
        value = raw_data.get(key)
        if value is not None:
            return value
        return default_value

    preprocessed_data = {}

    preprocessed_data["SIGUN_NM"] = get_value_or_default("SIGUN_NM", "미확인")
    preprocessed_data["SIGUN_CD"] = int(get_value_or_default("SIGUN_CD", "0"))
    preprocessed_data["BIZPLC_NM"] = get_value_or_default("BIZPLC_NM", "미확인")
    preprocessed_data["BSN_STATE_NM"] = get_value_or_default("BSN_STATE_NM", "미확인")
    preprocessed_data["LOCPLC_AR"] = float(get_value_or_default("LOCPLC_AR", "0.0"))
    preprocessed_data["GRAD_FACLT_DIV_NM"] = get_value_or_default(
        "GRAD_FACLT_DIV_NM", "미확인"
    )
    preprocessed_data["MALE_ENFLPSN_CNT"] = int(
        get_value_or_default("MALE_ENFLPSN_CNT", "0")
    )
    preprocessed_data["YY"] = get_value_or_default("YY", "0")
    preprocessed_data["MULTI_USE_BIZESTBL_YN"] = (
        1 if raw_data.get("MULTI_USE_BIZESTBL_YN") == "Y" else 0
    )
    preprocessed_data["GRAD_DIV_NM"] = get_value_or_default("GRAD_DIV_NM", "미확인")
    preprocessed_data["TOT_FACLT_SCALE"] = float(
        get_value_or_default("TOT_FACLT_SCALE", "0.0")
    )
    preprocessed_data["FEMALE_ENFLPSN_CNT"] = int(
        get_value_or_default("FEMALE_ENFLPSN_CNT", "0")
    )
    preprocessed_data["BSNSITE_CIRCUMFR_DIV_NM"] = get_value_or_default(
        "BSNSITE_CIRCUMFR_DIV_NM", "미확인"
    )
    preprocessed_data["SANITTN_INDUTYPE_NM"] = get_value_or_default(
        "SANITTN_INDUTYPE_NM", "미확인"
    )
    preprocessed_data["SANITTN_BIZCOND_NM"] = get_value_or_default(
        "SANITTN_BIZCOND_NM", "미확인"
    )
    preprocessed_data["TOT_EMPLY_CNT"] = int(get_value_or_default("TOT_EMPLY_CNT", "0"))
    preprocessed_data["REFINE_LOTNO_ADDR"] = get_value_or_default(
        "REFINE_LOTNO_ADDR", "미확인"
    )
    preprocessed_data["REFINE_ROADNM_ADDR"] = get_value_or_default(
        "REFINE_ROADNM_ADDR", "미확인"
    )
    preprocessed_data["REFINE_ZIP_CD"] = get_value_or_default("REFINE_ZIP_CD", "00000")
    preprocessed_data["REFINE_WGS84_LOGT"] = get_value_or_default(
        "REFINE_WGS84_LOGT", "00.00000"
    )
    preprocessed_data["REFINE_WGS84_LAT"] = get_value_or_default(
        "REFINE_WGS84_LAT", "00.00000"
    )

    # 유일성 체크를 위한 IDENTIFIER 필드 생성
    preprocessed_data[
        "IDENTIFIER"
    ] = f'{raw_data.get("REFINE_LOTNO_ADDR")} {raw_data.get("BIZPLC_NM")}'

    license_date = raw_data.get("LICENSG_DE")
    if license_date is not None:
        # 날짜 형식이 YYYY-mm-dd일 때
        if bool(re.match(r"\d{4}-\d{2}-\d{2}", license_date)):
            preprocessed_data["LICENSG_DE"] = license_date
        # 날짜 형식이 YYYYmmdd일 때
        else:
            preprocessed_data[
                "LICENSG_DE"
            ] = f"{license_date[:4]}-{license_date[4:6]}-{license_date[6:8]}"
    else:
        preprocessed_data["LICENSG_DE"] = "0000-00-00"

    closed_date = raw_data.get("CLSBIZ_DE")
    if closed_date is not None:
        # 날짜 형식이 YYYY-mm-dd일 때
        if bool(re.match(r"\d{4}-\d{2}-\d{2}", closed_date)):
            preprocessed_data["CLSBIZ_DE"] = closed_date
        # 날짜 형식이 YYYYmmdd일 때
        else:
            preprocessed_data[
                "CLSBIZ_DE"
            ] = f"{closed_date[:4]}-{closed_date[4:6]}-{closed_date[6:8]}"
    else:
        preprocessed_data["CLSBIZ_DE"] = "0000-00-00"

    return preprocessed_data


# 전처리된 데이터를 실제 저장하는 함수
def save_raw_data(total_list, page):
    for raw_data in total_list:
        if RawData.objects.filter(
            IDENTIFIER=f'{raw_data.get("REFINE_LOTNO_ADDR")} {raw_data.get("BIZPLC_NM")}'
        ).exists():
            continue

        preprocessed_data = preprocess_data(raw_data)

        serializer = RawDataSerializer(data=preprocessed_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return {
                "status": status.HTTP_400_BAD_REQUEST,
                "error_page": page,
                "error_point": raw_data.get("BIZPLC_NM"),
            }

    return {"status": status.HTTP_201_CREATED, "count": len(total_list)}


# 페이지별로 데이터 저장을 요청하는 함수
@shared_task
def raw_data_handler():
    for business_type in business_type_list:
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

            result = save_raw_data(total_list, i + 1)
            if result.get("status") == 201:
                continue
            else:
                return {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "error_page": result.get("error_page"),
                    "error_point": result.get("error_point"),
                }

    return {"status": status.HTTP_201_CREATED, "count": len(total_list)}
