from django.db import models

"""
주의: 조회수는 있다고 가칭하고 로직 구현을 위해 추가한 없는 필드입니다.
따라서 이 브렌치는, 참고용으로만 보시고, 실제로는 이 브렌치를 머지하거나 사용하지 않아야 합니다.
"""


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
