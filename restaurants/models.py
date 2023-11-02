from django.db import models


class RawData(models.Model):
    SIGUN_NM = models.CharField(max_length=255)
    SIGUN_CD = models.CharField(max_length=255)

    LICENSG_DE = models.CharField(max_length=255)
    CLSBIZ_DE = models.CharField(max_length=255)
    YY = models.CharField(max_length=4)

    BIZPLC_NM = models.CharField(max_length=255)
    BSN_STATE_NM = models.CharField(max_length=255)
    GRAD_FACLT_DIV_NM = models.CharField(max_length=255)
    GRAD_DIV_NM = models.CharField(max_length=255)
    BSNSITE_CIRCUMFR_DIV_NM = models.CharField(max_length=255)
    SANITTN_INDUTYPE_NM = models.CharField(max_length=255)
    SANITTN_BIZCOND_NM = models.CharField(max_length=255)

    LOCPLC_AR = models.FloatField()
    TOT_FACLT_SCALE = models.FloatField()

    MALE_ENFLPSN_CNT = models.PositiveIntegerField()
    FEMALE_ENFLPSN_CNT = models.PositiveIntegerField()
    TOT_EMPLY_CNT = models.PositiveIntegerField()

    MULTI_USE_BIZESTBL_YN = models.BooleanField()

    REFINE_ZIP_CD = models.CharField(max_length=5)
    REFINE_ROADNM_ADDR = models.CharField(max_length=255)
    REFINE_LOTNO_ADDR = models.CharField(max_length=255)

    REFINE_WGS84_LAT = models.CharField(max_length=255)
    REFINE_WGS84_LOGT = models.CharField(max_length=255)

    IDENTIFIER = models.CharField(unique=True, max_length=255)


class Restaurant(models.Model):
    location_name = models.CharField(max_length=255)
    location_code = models.CharField(max_length=255)

    restaurant_name = models.CharField(max_length=255)
    business_status_name = models.CharField(max_length=255)

    zip_code = models.CharField(max_length=5)
    lot_address = models.CharField(max_length=255)
    road_address = models.CharField(max_length=255)

    lat = models.CharField(max_length=255)
    logt = models.CharField(max_length=255)

    rating = models.FloatField()
