from django.db import models


class Restaurant(models.Model):
    location_name = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="시군명"
    )
    location_code = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="시군코드"
    )
    restaurant_name = models.CharField(max_length=128, verbose_name="사업장명")
    license_date = models.CharField(max_length=128, verbose_name="인허가일자")
    business_status_name = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="영업상태명"
    )
    closed_date = models.CharField(max_length=128, verbose_name="폐업일자")
    location_area = models.FloatField(default=0, verbose_name="소재지면적")
    water_supply_facility_name = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="급수시설구분명"
    )
    male_worker_count = models.FloatField(default=0, verbose_name="남성종사자수")
    year = models.CharField(max_length=128, blank=True, null=True, verbose_name="년도")
    multi_use_yn = models.CharField(
        max_length=10, default="N", blank=True, null=True, verbose_name="다중이용업소여부(Y/N)"
    )
    grade_division_name = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="등급구분명"
    )
    total_facility_scale = models.FloatField(default=0, verbose_name="총시설규모")
    female_worker_count = models.FloatField(default=0, verbose_name="여성종사자수")
    business_site_around_name = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="영업장주변구분명"
    )
    clean_industry_name = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="위생업종명"
    )
    clean_business_type = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="위생업태명"
    )

    total_worker_count = models.FloatField(default=0, verbose_name="총종업원수")
    road_address = models.CharField(max_length=128, verbose_name="소재지도로명주소")
    lot_num_address = models.CharField(max_length=128, verbose_name="소재지지번주소")
    zip_code = models.CharField(max_length=128, verbose_name="소재지우편번호")
    latitude = models.FloatField(verbose_name="위도")
    longitude = models.FloatField(verbose_name="경도")

    rating = models.FloatField(default=0, verbose_name="평점")
    restaurant_code = models.CharField(
        max_length=200, unique=True, verbose_name="사업장코드"
    )

    def __str__(self):
        return self.restaurant_name