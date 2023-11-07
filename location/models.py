from django.db import models


class Location(models.Model):
    do_si = models.CharField(max_length=20)
    sgg = models.CharField(max_length=20)
    latitude = models.FloatField(verbose_name="위도")
    longitude = models.FloatField(verbose_name="경도")
    views = models.IntegerField(default=0, verbose_name="조회 수")

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.do_si}|{self.sgg} 위/경도 : [{self.latitude}, {self.longitude}] 조회 수: {self.views}"
