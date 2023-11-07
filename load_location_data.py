"""
csv 파일인 location_data를 model에 저장하는 코드

주기적으로 바뀌는 데이터가 아니라 데이터가 바뀔 때마다 해당 파일을 실행시켜 DB를 업데이트 해주면 된다.
"""

import os
import django
from django.core.cache import cache
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from location.models import Location


def load_location_data():
    fields = {"do-si": "do_si", "sgg": "sgg", "lat": "latitude", "lon": "longitude"}

    # csv 파일 load
    location_data = pd.read_csv("static/data/sgg_lat_lon.csv")
    # db에 맞게 field명 rename
    location_data.rename(columns=fields, inplace=True)
    # dict 형태로 반환
    location_data = location_data.to_dict(orient="records")

    return location_data


def save_to_model():
    location_data = load_location_data()

    # 데이터 저장
    for data in location_data:
        Location.objects.update_or_create(
            defaults=data, do_si=data["do_si"], sgg=data["sgg"]
        )


if __name__ == "__main__":
    save_to_model()

    # 값에 변경이 있을 수 있으므로, 캐싱된 지역 데이터 삭제
    cache.delete("location/")
