"""
csv 파일인 location_data를 model에 저장하는 코드

주기적으로 바뀌는 데이터가 아니라 데이터가 바뀔 때마다 해당 파일을 실행시켜 DB를 업데이트 해주면 된다.
"""
from django.core.cache import cache

from celery import shared_task

import os
import django
import pandas as pd
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from location.models import Location


@shared_task
def load_location_data():
    fields = {"do-si": "do_si", "sgg": "sgg", "lat": "latitude", "lon": "longitude"}

    # csv 파일 load
    location_data = pd.read_csv("static/data/sgg_lat_lon.csv")
    # db에 맞게 field명 rename
    location_data.rename(columns=fields, inplace=True)
    # dict 형태로 반환
    location_data = location_data.to_dict(orient="records")

    return location_data


# docker 환경에서 celery 미적용시: 15.449251s
# docker 환경에서 celery 적용시: 6.58139s
@shared_task
def save_to_model():
    start = time.time()

    location_data = load_location_data()

    # location_data라는 이름의 캐시가 있다면 삭제
    # 캐시는 실시간 반영이 되지 않기 때문
    cache.delete("location_data")

    # 데이터 저장
    for data in location_data:
        Location.objects.update_or_create(
            defaults=data, do_si=data["do_si"], sgg=data["sgg"]
        )

    # 지역 데이터를 전부 location_data라는 이름으로 캐싱
    cache.set("location_data", Location.objects.all())

    print(f"실행시간: {time.time() - start}")
